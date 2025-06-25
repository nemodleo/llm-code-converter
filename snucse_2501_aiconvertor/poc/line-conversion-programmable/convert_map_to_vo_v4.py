#!/usr/bin/env python3
"""
Simple script to refactor Java files line-by-line: replace Map operations with Value Object getters/setters
using Ollama's Python client.

Usage:
    pip install ollama
    python convert_map_to_vo.py --input path/to/Original.java \
                                --vo path/to/YourVoClass.java \
                                --output path/to/Refactored.java \
                                [--model llama3.2]
"""
import ollama
from typing import List, Tuple, Set
from pathlib import Path
import argparse, json, re, sys


def load_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def slurp(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def spit(path: str, txt: str):
    Path(path).write_text(txt, encoding="utf-8")

def _parse_block(block: str) -> Tuple[str, str]:
    inp = out = None
    for ln in block.splitlines():
        if ln.startswith("Input:"):
            inp = ln[len("Input:"):].strip()
        elif ln.startswith("Output:"):
            out = ln[len("Output:"):].strip()
    if inp is None or out is None:
        raise ValueError(f"Malformed example block:\n{block}")
    return inp, out


def load_examples_txt(path: str) -> List[Tuple[str, str]]:
    if not Path(path).exists():
        import pdb; pdb.set_trace()
        return []
    raw = slurp(path)
    blocks = [b for b in re.split(r"\n\s*\n", raw) if b.strip() and not b.strip().startswith("#")]
    return [_parse_block(b) for b in blocks]


def save_examples_txt(path: str, examples: List[Tuple[str, str]]):
    with open(path, "w", encoding="utf-8") as f:
        for inp, out in examples:
            f.write(f"Input: {inp}\n")
            f.write(f"Output: {out}\n\n")


def examples_to_prompt(exs: List[Tuple[str, str]]) -> str:
    buf = ["<examples>"]
    for i, o in exs:
        buf.append("<example>")
        buf.append(f"Input: {i}")
        buf.append(f"Output: {o}")
        buf.append("</example>")
    buf.append("</examples>")
    return "\n".join(buf)

def dedup_preserve_order(pairs: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """[(in,out), …] 리스트에서 첫 등장 순서를 보존하며 중복 제거"""
    return list(dict.fromkeys(pairs))   # 3.7+ dict 는 insertion-ordered


def convert_line(line: str, vo_definition: str, ex_block: str, model: str) -> str:
    """
    Uses Ollama chat endpoint to convert a single Java line that uses Map operations into
    VO getter/setter style based on the provided VO class. Unchanged if no Map usage.
    Preserves original leading whitespace. In-context examples guide the model.
    """
    indent = re.match(r"\s*", line).group(0)
    code = line.strip()

    # Skip lines without map operations or MapDataUtil usage
    if not re.search(r"\bmap\.(get|put|remove)\b|Map", code):
        return line, False

    # In-context examples
    # Build prompt (concise)
    prompt = f"""

<vo_definition>
{vo_definition}
</vo_definition>

Using the above Value Object definition, transform the following Java line that uses Map operations into the corresponding VO getter/setter style.

{ex_block}

<rules>
1. If the input line already uses the VO, return it unchanged.
2. Otherwise, *only* do the minimum Map-to-VO replacements shown in the examples.
3. Preserve every other character (whitespace, semicolons, generics, throws-clauses, etc.).
4. Return exactly one Java line. No comments, no blank lines, no extra text.
</rules>

Input: {code}
Output: ```java
"""

    # Call Ollama's chat API
    resp = ollama.chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a code transformer. "
                    "You MUST respond with exactly one Java statement "
                    "(no comments, no markdown, no numbering, no extra text)."

                    # "You are a code transformer. "
                    # "Respond with exactly one valid Java statement. "
                    # "Do not include <thinking>, or any explanation. "
                    # "Just return raw Java code on a single line."
                )
            },
            {
                'role':'user', 'content': prompt
            }
        ]
    )
    # Extract generated text
    if isinstance(resp, dict) and 'message' in resp:
        content = resp['message']['content']
    else:
        content = resp.message.content
    print(f"\033[92m{prompt}\033[0m")
    # Strip everything except the raw line
    content = content.replace('```java', '').replace('```', '').strip() #!!!!!!!!!!!
    transformed = content.strip().splitlines()[0]
    print(f"\033[94m{transformed}\033[0m")

    # Reapply original indentation
    line_out = indent + transformed
    return line_out + ('\n' if not line_out.endswith('\n') else ''), True


def main():
    parser = argparse.ArgumentParser(
        description="Refactor Java Map calls to VO getters/setters using Ollama."
    )
    parser.add_argument('--input', '-i', required=False, help="Path to the original Java file.")
    parser.add_argument('--vo', '-v', required=False, help="Path to the Value Object Java file.")
    parser.add_argument('--output', '-o', required=False, help="Path to save the refactored file.")
    parser.add_argument(
        '--model', '-m', default='llama3.1:8b',
        help="Ollama model to use (e.g., llama3.2, mistral)."
    )
    parser.add_argument(
        '--answer', '-a', default=None,
        help="GT answer file."
    )
    parser.add_argument("-e", "--examples", required=False,
                    help="TEXT file with in-context examples")
    parser.add_argument("--examples_out", default="new-in-context-examples.txt")
    args = parser.parse_args()

    original = load_file(args.input)
    if not args.answer:
        vo_def = load_file(args.vo)
        examples = load_examples_txt(args.examples)
        prompt_blk = examples_to_prompt(examples)

    if args.answer is not None:
        output = load_file(args.output)
        out_lines = output.splitlines(True)
        orig_lines = original.splitlines(True)
        answer = load_file(args.answer)
        answer_lines = answer.splitlines(True)

        new_ex: Set[Tuple[str, str]] = set()

        # assert len(answer_lines) == len(out_lines), \
        #     f"Answer file has {len(answer_lines)} lines, output has {len(out_lines)} lines."
        if len(answer_lines) != len(out_lines):
            print(f"Answer file has {len(answer_lines)} lines, output has {len(out_lines)} lines.")
        
        for i, (ans_line, out_line, orig_line) in enumerate(zip(answer_lines, out_lines, orig_lines)):
            if ans_line != out_line:
                print(f"  ====Mismatch:\nLine: {orig_line.strip()}\nExpected: {ans_line.strip()}\nGot: {out_line.strip()}")
                new_ex.add((orig_line.strip(), ans_line.strip()))

            else:
                # print(f"Match: {ans_line.strip()}")
                pass

        # if new_ex:
        #     merged = dedup_preserve_order(examples + list(new_ex))

        #     save_examples_txt(args.examples_out, merged)
        #     print(f"[INFO] merged examples → {args.examples_out}")
        # else:
        #     print("[INFO] perfect match; examples unchanged")

        print(len(new_ex), "errors found")
        exit(0)


    out_lines = []
    out_modified_lines = []
    for line_no, line in enumerate(original.splitlines(True)):  # preserve newline
        if not line.strip():
            out_lines.append(line)
            continue
        try:
            new_line, changed = convert_line(line, vo_def, prompt_blk, args.model)
        except Exception as e:
            print(e)
            new_line = line
        out_lines.append(new_line)
        if changed:
            out_modified_lines.append((line, new_line))

    write_file(args.output, ''.join(out_lines))
    print(f"Refactored file written to: {args.output}")

    # compare answer file and the output file -> and then get diff

    # Print modified lines for debugging
    print("\nModified lines:")
    write_file(args.output + '.orig', ''.join([orig for orig, new in out_modified_lines]))
    write_file(args.output + '.new', ''.join([new for orig, new in out_modified_lines]))
    print(f"Original lines written to: {args.output}.orig")
    print(f"New lines written to: {args.output}.new")



if __name__ == '__main__':
    main()
