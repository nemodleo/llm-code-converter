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
import argparse
import re
import ollama


def load_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def convert_line(line: str, vo_definition: str, model: str) -> str:
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
    examples = """
<examples>
<example>
Input: }
Output: }
</example>

<example>
Input: import javax.annotation.Resource;
Output: import javax.annotation.Resource;
</example>

<example>
Input: map.remove("FOO");
Output: map.removeFoo();
</example>

<example>
Input: String x = map.get("BAR");
Output: String x = map.getBar();
</example>

<example>
Input: map.put("BAZ", someValue);
Output: map.setBaz(someValue);
</example>

<example>
Input: ArrayList<Map> result = null;
Output: ArrayList<SecuritiesInqrPritMgmtVo> result = null;
</example>

<example>
Input: MapDataUtil.setString(pDoc, "TRNS_DATE_FROM", trnsDateFrom);
Output: pDoc.setTrnsDateFrom(trnsDateFrom);
</example>

<example>
Input: MapDataUtil.setBigDecimal(result, "ACML_PRRT", acmlPrrt);
Output: result.setACML_PRRT(acmlPrrt);
</example>
</examples>

"""
    # Build prompt (concise)
    prompt = f"""

<vo_definition>
{vo_definition}
</vo_definition>
Using the above Value Object definition, transform the following Java line that uses Map operations into the corresponding VO getter/setter style.

{examples}
Transform only Map relevant calls into the corresponding VO operations (getters/setters). If the line has none of these, return it unchanged.

Input: {code}
Output:"""

    # Call Ollama's chat API
    resp = ollama.chat(
        model=model,
        messages=[{ "role": "system", "content": "You are a code transformer. You MUST respond with exactly one Java statement (no comments, no markdown, no numbering, no extra text)." },{'role':'user', 'content': prompt}]
    )
    # Extract generated text
    if isinstance(resp, dict) and 'message' in resp:
        content = resp['message']['content']
    else:
        content = resp.message.content
    print(f"\033[92m{prompt}\033[0m")
    # Strip everything except the raw line
    transformed = content.strip().splitlines()[0]
    print(f"\033[94m{transformed}\033[0m")

    # Reapply original indentation
    line_out = indent + transformed
    return line_out + ('\n' if not line_out.endswith('\n') else ''), True


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
    args = parser.parse_args()

    original = load_file(args.input)
    vo_def = load_file(args.vo)

    out_lines = []
    out_modified_lines = []
    for line in original.splitlines(True):  # preserve newline
        if not line.strip():
            out_lines.append(line)
            continue
        try:
            new_line, changed = convert_line(line, vo_def, args.model)
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
