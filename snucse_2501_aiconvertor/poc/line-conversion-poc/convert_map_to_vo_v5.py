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
from openai import OpenAI
import javalang, string
from javalang.parser import JavaSyntaxError

client = OpenAI()


def load_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# ── helpers for I/O -----------------------------------------------------------
def load_text(p: Path)  -> str: p = Path(p); return p.read_text(encoding='utf-8')
def save_text(p: Path,s)-> None: Path(p).write_text(s, encoding='utf-8')
# ------------------------------------------------------------------------------


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


def convert_line(line: str, vo_definition: str, ex_block: str, model: str, rule_text: str = None, normalize_vars = False) -> str:
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

    # Skip lines with import statement
    if code.startswith("import ") or code.startswith("package "):
        return line, False
    
    if normalize_vars:
        # Normalize
        processed_code, reverse_map = normalize_variable_names(code)
    else:
        processed_code = code


    # In-context examples
    # Build prompt (concise)
    conversion_rule_block = (
        f"\n<conversion_rule>\n{rule_text}\n</conversion_rule>\n"
        if rule_text else ""
    )

    prompt = f"""

<vo_definition>
{vo_definition}
</vo_definition>

Using the above Value Object definition, transform the following Java line that uses Map operations into the corresponding VO getter/setter style.

{ex_block}
{conversion_rule_block}

<rules>
1. If the input line already uses the VO, return it unchanged.
2. Otherwise, *only* do the minimum Map-to-VO replacements shown in the examples.
3. Preserve every other character (whitespace, semicolons, generics, throws-clauses, parentheses, etc.).
4. Return exactly one Java line. No comments, no blank lines, no extra text.
5. The output must not contain MapDataUtil.* anywhere (including inside arguments).
</rules>


Input: {processed_code}
Output: 
"""

    # Call Ollama's chat API
    resp = ollama.chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a code transformer. "
                    "You MUST respond with exactly one Java line "
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
        ],
        options={"temperature": 0, "top_p": 1, "top_k": 2}   # two best beams
    )
    # Extract generated text
    if isinstance(resp, dict) and 'message' in resp:
        content = resp['message']['content']
    else:
        content = resp.message.content
    print(f"\033[92m{prompt}\033[0m")
    print(f"\033[93m{content}\033[0m")
    # Extract code from code block if present, otherwise use full content
    if '```' in content:
        content = content[content.find('```')+3:]  # Skip opening ```
        if content.startswith('java\n'):  # Handle ```java
            content = content[5:]
        content = content[:content.rfind('```')]  # Remove closing ```
    transformed = content.strip().splitlines()[0]
    print(f"\033[94m{transformed}\033[0m")

    if normalize_vars:
        # Unnormalize
        transformed = unnormalize_variable_names(transformed, reverse_map)
    
    print("Line:", line.strip())
    if normalize_vars:
        print("Normalized:", processed_code.strip())
        print("Unnormalized:", transformed.strip())

    # Reapply original indentation
    line_out = indent + transformed
    return line_out + ('\n' if not line_out.endswith('\n') else ''), True

def convert_line_gpt4(line: str, vo_definition: str, ex_block: str, model: str = "gpt-4-turbo") -> Tuple[str, bool]:
    """
    Converts a single Java line using GPT-4 API to replace Map operations
    with VO getter/setter style, matching original convert_line functionality.
    """
    indent = re.match(r"\s*", line).group(0)
    code = line.strip()

    # Skip lines without map operations or MapDataUtil usage
    if not re.search(r"\bmap\.(get|put|remove)\b|Map", code):
        return line, False

    prompt = f"""
Transform the following Java line that uses Map operations into the corresponding VO getter/setter style.

{ex_block}

<rules>
1. If the input line already uses the VO, return it unchanged.
2. Otherwise, *only* do the minimum Map-to-VO replacements shown in the examples.
3. Preserve every other character (whitespace, semicolons, generics, throws-clauses, etc.).
4. Return exactly one Java line. No comments, no blank lines, no extra text.
</rules>

Input: {code}
Output:
"""

    # Call GPT-4 API
    response = client.chat.completions.create(model=model,
    messages=[
        {"role": "system", "content": "You are a code transformer. You MUST respond with exactly one Java line (no comments, markdown, numbering, or extra text)."},
        {"role": "user", "content": prompt}
    ])

    content = response.choices[0].message.content.strip()

    print(f"\033[92m{prompt}\033[0m")
    print(f"\033[93m{content}\033[0m")
    # Extract code if markdown formatting is returned
    if '```' in content:
        content = content[content.find('```')+3:]  # skip opening ```
        if content.startswith('java\n'):
            content = content[5:]
        content = content[:content.rfind('```')]  # remove closing ```


    transformed = content.strip().splitlines()[0]
    print(f"\033[94m{transformed}\033[0m")

    # Reapply original indentation
    line_out = indent + transformed
    if not line_out.endswith('\n'):
        line_out += '\n'

    return line_out, True

# ----------------------------------------------------------------------
# 1) NORMALISE ONLY *VARIABLE* IDENTIFIERS
# ----------------------------------------------------------------------
def normalize_variable_names(code: str) -> tuple[str, dict[str, str]]:
    """
    Same logic as before, but now:
      • remembers whether the incoming string ended with \n or \r\n
      • appends the very same line-ending to the normalised string
    """
    # ── 1) Remember the original terminator ('' | '\n' | '\r\n') ─────────
    newline = ''
    if code.endswith('\r\n'):
        newline, code = '\r\n', code[:-2]
    elif code.endswith('\n'):
        newline, code = '\n', code[:-1]

    # ── 2) Run the normalisation exactly as before ───────────────────────
    tokens = list(javalang.tokenizer.tokenize(code))

    var_map: dict[str, str] = {}
    reverse:  dict[str, str] = {}
    counter = 1
    out: list[str] = []

    for i, tok in enumerate(tokens):
        if not isinstance(tok, javalang.tokenizer.Identifier):
            out.append(tok.value)
            continue

        name = tok.value
        prev_val = tokens[i - 1].value if i else ''
        next_val = tokens[i + 1].value if i + 1 < len(tokens) else ''
        is_type  = name[0].isupper()
        is_call  = next_val == '('
        is_field = prev_val == '.'
        is_ctor  = prev_val == 'new'

        if is_type or is_call or is_field or is_ctor:
            out.append(name)
            continue

        if name not in var_map:
            placeholder = f"var{counter}"
            var_map[name] = placeholder
            reverse[placeholder] = name
            counter += 1
        out.append(var_map[name])

    normalised = _reconstruct_code(out) + newline
    return normalised, reverse

# ----------------------------------------------------------------------
# 2) PUT TOKENS BACK TOGETHER WITH NORMAL SPACING  (generic-aware)
# ----------------------------------------------------------------------
def _reconstruct_code(tokens: list[str]) -> str:
    """
    Rebuild a Java line with “natural” spacing.

    * No blank before   . , ; ) ] : ( [
    * One blank after   ,          (unless at end of line)
    * No blank after    (  .  @  < [
    * No blank after '<'  and  no blank before '>'  **when inside generics**.
    * Otherwise one blank around binary ops such as > < >= <= == != && ||.
    """
    NO_SPACE_BEFORE = {'.', ',', ';', ')', ']', ':', '[', '('}
    NO_SPACE_AFTER  = {'(', '.', '@', '<', '['}

    CONTROL_KW = {'if', 'for', 'while', 'switch', 'catch',
                  'synchronized', 'assert'}

    out: list[str] = []
    angle_depth = 0

    for i, tok in enumerate(tokens):
        if i:                                 # not the first token
            prev = tokens[i - 1]

            # -------- generic-specific rules ---------------------------
            if prev == '<' and angle_depth > 0:
                # never space right after '<T'
                pass
            elif tok == '>' and angle_depth > 0:
                # never space before '>'
                pass
            # -------- control-flow “kw (” spacing ----------------------
            elif tok == '(' and prev in CONTROL_KW:
                out.append(' ')
            # -------- standard rule ------------------------------------
            elif tok not in NO_SPACE_BEFORE and prev not in NO_SPACE_AFTER:
                out.append(' ')

            # ensure exactly one space *after* a comma
            if prev == ',' and out[-1] != ' ':
                out.append(' ')

        out.append(tok)

        # -------- maintain angle-bracket depth -------------------------
        if tok == '<':
            angle_depth += 1
        elif tok == '>' and angle_depth:
            angle_depth -= 1

    return ''.join(out)

# Put this near the top of the file once
VAR_TOKEN = re.compile(r'\bvar\d+\b')

# ----------------------------------------------------------------------
# RESTORE ORIGINAL VARIABLE NAMES **WITHOUT TOUCHING WHITESPACE**
# ----------------------------------------------------------------------
def unnormalize_variable_names(code: str, reverse_map: dict[str, str]) -> str:
    """
    Replace each placeholder varN with its original identifier.
    Whitespace, punctuation, and new-lines are left exactly as they were.
    """
    def repl(match: re.Match) -> str:
        placeholder = match.group(0)
        return reverse_map.get(placeholder, placeholder)

    return VAR_TOKEN.sub(repl, code)


# ── one-shot rule induction ────────────────────────────────────────────
def infer_rule(ex_block: str, model: str) -> str:
    """
    Ask Ollama to express *in plain English* (or pseudo-code) the mapping
    it observes in the examples.  We keep it deterministic.
    """
    prompt = f"""
The following are I/O examples of a code-transformation task.

{ex_block}

### Task ① – Rule discovery
Infer **as many concrete transformation rules as possible** that explain how
each Input becomes its Output.  
Cover, for example:

• MapDataUtil.get*/set*   →  VO getter/setter  
• map.get/put             →  VO getter/setter  
• new Map / ArrayList<Map> → new <VO> / ArrayList<VO>  
• Method parameters and return types changing from Map to VO  
• Key-literal → property-name conversion (describe the algorithm)  
• Any other recurring change you detect.

Even if you’re unsure, include plausible sub-rules (mark them “tentative”).

### Task ② – Output format
Return **ONLY** the rulebook, as an ordered list:

1. <first rule>
2. <second rule>
…

Avoid examples, explanations of reasoning, or any additional prose outside the
numbered list.
"""
    resp = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert Java reverse-engineer."},
            {"role": "user",   "content": prompt}
        ],
        options={"temperature": 0, "top_p": 0.0}     # fully deterministic
    )
    rule = resp["message"]["content"] if isinstance(resp, dict) else resp.message.content
    return rule.strip()


# ----------------------------------------------------------------------
#  helper ➊  – find the *innermost* MapDataUtil.*(...) span
# ----------------------------------------------------------------------
import textwrap

INNER_MD_RE = re.compile(
    r'''
    MapDataUtil\.\w+\s*       # qualifier.getString / setString / …
    \(\s*                     # opening parenthesis
       (?:[^()]*              # anything but parens
         | \( [^()]* \)       # or a balanced () pair – one level deep only
       )*?                    #   …repeat (lazy)
    \)                        # closing parenthesis
    ''', re.VERBOSE
)

# ----------------------------------------------------------------------
# helper 1  — convert inner expr using LLM
# ----------------------------------------------------------------------
def innermost_mapdatautil(code: str) -> tuple[str, tuple[int, int]] | None:
    positions = [m.start() for m in re.finditer(r'MapDataUtil\.', code)]
    if not positions:
        return None

    def match_span(pos: int):
        depth = 0
        i = pos
        while i < len(code):
            ch = code[i]
            if ch == '(': depth += 1
            elif ch == ')':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    # swallow an eventual trailing ‘;’ (but keep blanks)
                    j = end
                    while j < len(code) and code[j].isspace():
                        j += 1
                    if j < len(code) and code[j] == ';':
                        end = j + 1
                    return pos, end
            i += 1
        return None

    spans = [match_span(p) for p in positions if match_span(p)]
    if not spans:
        return None
    start, end = spans[-1]     # innermost
    return code[start:end], (start, end)

# ----------------------------------------------------------------------
#  helper 2  – recursively peel the line using LLM
# ----------------------------------------------------------------------
def peel_nested(line: str,
                vo_def: str,
                prompt_blk: str,
                model: str,
                rule_text: str,
                normalize_vars: bool) -> str:
    """
    Replace innermost MapDataUtil.* with LLM rewrite, insert varₙ placeholders,
    and keep peeling until no MapDataUtil remains.  Then restore placeholders.
    """
    placeholders = []
    counter = 1
    work = line

    while "MapDataUtil." in work:
        inner = innermost_mapdatautil(work)
        if not inner:
            break
        snippet, (s, e) = inner

        # --- call existing convert_line on the *snippet* ----------------
        rewritten, _ = convert_line(
            snippet, vo_def, prompt_blk,
            model, rule_text, normalize_vars
        )
        # import pdb; pdb.set_trace()

        ph = f"__MD_PLACEHOLDER_{counter}__"
        placeholders.append((ph, rewritten.rstrip('\n')))
        counter += 1

        work = work[:s] + ph + work[e:]          # splice in the placeholder

    # At this point work has no MapDataUtil; send entire statement once
    final, _ = convert_line(
        work, vo_def, prompt_blk,
        model, rule_text, normalize_vars
    )

    # restore placeholders last-in-first-out
    for ph, repl in reversed(placeholders):
        final = final.replace(ph, repl)

    return final

# ── tiny façade around the existing per-file logic ----------------------------
def refactor_source(src: str,
                    vo_def: str,
                    prompt_blk: str,
                    *,
                    model: str,
                    rule_text: str | None,
                    normalise: bool) -> str:
    """
    Run the whole “read-▶transform-▶write” pipeline **on one source string**
    and return the new text.  This is the old `main()` loop factored out so
    we can re-use it for every file in a directory walk.
    """
    out_lines: list[str] = []

    for line in src.splitlines(keepends=True):
        if model.startswith("gpt"):
            new_line, _ = convert_line_gpt4(
                line, vo_def, prompt_blk, model
            )
        else:
            if "MapDataUtil." in line:
                new_line = peel_nested(
                    line, vo_def, prompt_blk,
                    model, rule_text, normalise
                )
            else:
                new_line, _ = convert_line(
                    line, vo_def, prompt_blk,
                    model, rule_text, normalise
                )
        out_lines.append(new_line)

    return ''.join(out_lines)


def main():
    parser = argparse.ArgumentParser(
        description="Refactor Java Map calls to VO getters/setters using Ollama."
    )
    parser.add_argument('--input', '-i', required=True, help="Path to the original Java file.")
    parser.add_argument('--vo', '-v', required=True, help="Path to the Value Object Java file.")
    parser.add_argument('--output', '-o', required=True, help="Path to save the refactored file.")
    parser.add_argument(
        '--model', '-m', default='llama3.1:8b',
        help="Ollama model to use (e.g., llama3.2, mistral)."
    )
    parser.add_argument(
        '--answer', '-a', default=None,
        help="GT answer file."
    )
    parser.add_argument(
        '--deduce-rule', '-d', action='store_true',
        help="Whether to deduce the conversion rules from the examples."
    )
    parser.add_argument(
        '--normalize-vars', '-n', action='store_true',
        help="Whether to normalize variable names before conversion."
    )
    parser.add_argument(
        '--peel-nested', '-p', action='store_true',
        help="Whether to peel nested MapDataUtil statements."
    )
    parser.add_argument("-e", "--examples", required=True,
                    help="TEXT file with in-context examples")
    parser.add_argument("--examples_out", default="new-in-context-examples.txt")
    args = parser.parse_args()

    input_path = Path(args.input)
    vo_def = load_file(args.vo)
    examples = load_examples_txt(args.examples)
    prompt_blk = examples_to_prompt(examples)

    if args.deduce_rule:
        rule_text  = infer_rule(prompt_blk, args.model)
        print("[INFO] inferred rule →", rule_text)
        input('continue? y/n')
    else:
        rule_text = None

        # ───────────────── directory mode ─────────────────
    if input_path.is_dir():
        java_files = sorted(input_path.rglob("*.java"))
        if not java_files:
            print("No *.java found under", input_path);     sys.exit(0)

        print(f"\n⚠  {len(java_files)} Java files will be **overwritten** "
              f"under {input_path} .  Proceed? [y/N] ", end='', flush=True)
        if input().strip().lower() != 'y':
            print("Aborted.");  sys.exit(0)

        for jf in java_files:
            out_lines = []
            out_modified_lines = []
            for line_no, line in enumerate(load_text(jf).splitlines(True)):  # preserve newline
                if not line.strip():
                    out_lines.append(line)
                    continue
                if args.model.startswith('gpt'):
                    new_line, changed = convert_line_gpt4(line, vo_def, prompt_blk, args.model)
                else:
                    if "MapDataUtil." in line:
                        new_line = peel_nested(
                            line, vo_def, prompt_blk,
                            args.model, rule_text, args.normalize_vars
                        )
                        changed  = new_line.strip() != line.strip()
                    elif "--->" in line:
                        # If the line contains a comment with "--->", skip it
                        new_line = line
                        changed = False
                    else:
                        new_line, changed = convert_line(
                            line, vo_def, prompt_blk, args.model,
                            rule_text, args.normalize_vars
                        )
                out_lines.append(new_line)
            new_src = ''.join(out_lines)
            save_text(jf, new_src)


        print("\nDone.")
        return  

    # if args.answer is not None:
    #     output = load_file(args.output)
    #     out_lines = output.splitlines(True)
    #     orig_lines = original.splitlines(True)
    #     answer = load_file(args.answer)
    #     answer_lines = answer.splitlines(True)

    #     new_ex: Set[Tuple[str, str]] = set()

    #     if len(answer_lines) != len(out_lines):
    #         print(f"Answer file has {len(answer_lines)} lines, output has {len(out_lines)} lines.")

    #     for i, (ans_line, out_line, orig_line) in enumerate(zip(answer_lines, out_lines, orig_lines)):
    #         if ans_line != out_line:
    #             print(f"  ====Mismatch:\nLine: {orig_line.strip()}\nExpected: {ans_line.strip()}\nGot: {out_line.strip()}")
    #             normalized, reverse_map = normalize_variable_names(orig_line)
    #             print(f"Normalized: {normalized}")
    #             print()
    #             new_ex.add((orig_line.strip(), ans_line.strip()))

    #         else:
    #             pass

    #     if new_ex:
    #         merged = dedup_preserve_order(examples + list(new_ex))

    #         save_examples_txt(args.examples_out, merged)
    #         print(f"[INFO] merged examples → {args.examples_out}")
    #     else:
    #         print("[INFO] perfect match; examples unchanged")

    #     print(len(new_ex), "errors found")
    #     exit(0)

    else:
        original = load_file(args.input)

        out_lines = []
        out_modified_lines = []
        if args.answer is not None:
            answer = load_file(args.answer)
            answer_lines = answer.splitlines(True)

        new_ex: Set[Tuple[str, str]] = set()
        for line_no, line in enumerate(original.splitlines(True)):  # preserve newline
            if not line.strip():
                out_lines.append(line)
                continue
            if args.model.startswith('gpt'):
                new_line, changed = convert_line_gpt4(line, vo_def, prompt_blk, args.model)
            else:
                if "MapDataUtil." in line and args.peel_nested:
                    new_line = peel_nested(
                        line, vo_def, prompt_blk,
                        args.model, rule_text, args.normalize_vars
                    )
                    changed  = new_line.strip() != line.strip()
                else:
                    new_line, changed = convert_line(
                        line, vo_def, prompt_blk, args.model,
                        rule_text, args.normalize_vars
                    )
            out_lines.append(new_line)
            if changed:
                out_modified_lines.append((line, new_line))
            if args.answer is not None:
                ans_line = answer_lines[line_no]
                if ans_line != new_line:
                    print(f"  ====Mismatch:\nLine: {line.strip()}\nExpected: {ans_line.strip()}\nGot: {new_line.strip()}")
                    if args.normalize_vars:
                        normalized, reverse_map = normalize_variable_names(line)
                        print(f"Normalized: {normalized}")
                    print()
                    new_ex.add((line, ans_line))
                    import pdb;
                    pdb.set_trace()

        print(f"{len(new_ex)} errors found")
        for samples in new_ex:
            print(f"  {samples[0]} → {samples[1]}")
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
