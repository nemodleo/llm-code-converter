import ollama
import json
import sys
from difflib import unified_diff



class Agent:
    def __init__(self, system_prompt=""):
        self.messages = []
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    def __call__(self, user_prompt: str, clear_messages=True):
        if clear_messages:
            self.messages = self.messages[1:]
        self.messages.append({"role": "user", "content": user_prompt})
        response = ollama.chat(
            model='qwen3:8b',
            # model='llama3.2',
            messages=self.messages,
            options={"temperature": 0.0}
        )
        reply = response['message']['content']
        self.messages.append({"role": "assistant", "content": reply})
        return reply

import sys
from pathlib import Path
import javalang


def signature_from_method(node: javalang.tree.MethodDeclaration) -> str:
    """
    Re-assemble a pretty Java-style signature from a javalang MethodDeclaration.
    Example:
        "public static int foo(String a, int b) throws IOException"
    """
    mods   = " ".join(node.modifiers) if node.modifiers else ""
    rtype  = node.return_type.name if node.return_type else ""          # constructor has None
    params = ", ".join(
        f"{p.type.name}{'[]' * len(p.type.dimensions)} {p.name}"
        for p in node.parameters
    )
    throws = (
        " throws " + ", ".join(str(t) for t in node.throws)
        if node.throws
        else ""
    )
    pieces = [mods, rtype, node.name]
    pieces = [p for p in pieces if p]  # drop empty strings
    return f'{" ".join(pieces)}({params}){throws}'


def extract_methods(java_code: str):
    tree = javalang.parse.parse(java_code)
    names      = []
    signatures = []

    for path, node in tree.filter(javalang.tree.MethodDeclaration):
        # skip abstract/interface stubs – they have no body (node.body is None)
        if node.body is None:
            continue
        names.append(node.name)
        signatures.append(signature_from_method(node))

    return names, signatures

def extract_method_bodies(java_code: str, target_names: set[str]) -> dict:
    """
    From the given Java source, return {function_name: full_code} for functions in target_names.
    """
    method_map = {}
    tree = javalang.parse.parse(java_code)
    lines = java_code.splitlines()

    for path, node in tree.filter(javalang.tree.MethodDeclaration):
        if node.name not in target_names:
            continue
        if node.body is None:
            continue  # skip abstract/interface stubs

        start_line = node.position.line - 1
        # heuristic: find the matching closing brace
        brace_count = 0
        found = False
        for end_line in range(start_line, len(lines)):
            brace_count += lines[end_line].count("{")
            brace_count -= lines[end_line].count("}")
            if brace_count == 0 and "}" in lines[end_line]:
                found = True
                break

        if found:
            method_body = "\n".join(lines[start_line:end_line + 1])
            method_map[node.name] = method_body
        else:
            print(f"[WARN] Could not match braces for method {node.name}")

    return method_map

def matches_regardless_of_spacing(a: str, b: str) -> bool:
    return ''.join(a.split()) == ''.join(b.split())


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_java_signatures.py <SomeFile.java> [output.py]")
        sys.exit(1)

    java_path     = Path(sys.argv[1])
    output_py     = Path(sys.argv[2]) if len(sys.argv) >= 3 else Path("extracted_functions.py")

    java_code = java_path.read_text(encoding="utf-8")
    names, sigs = extract_methods(java_code)

    # Emit a tiny Python module
    banner = (
        "# Auto-generated from {}\n"
        "# Contains all *concrete* method signatures found in that file.\n\n"
    ).format(java_path.name)

    lines = [
        banner,
        f"function_names      = {names!r}\n",
        f"function_signatures = {sigs!r}\n",
    ]
    output_py.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {output_py}  ({len(names)} functions)")

if __name__ == "__main__":
    main()