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
    Preserves original leading whitespace.
    """
    # Capture leading indentation
    indent = re.match(r"\s*", line).group(0)
    code = line.strip()

    prompt = f"""
You are a Java refactoring tool. Given this Value Object class:
{vo_definition}
Convert the following Java code line:
{code}
- Replace any Map.get()/Map.put()/Map.remove() calls
  with corresponding VO.getXxx()/VO.setXxx()/VO.removeXxx() methods.
- If the line contains no Map operations, return it exactly as-is.
Provide only the transformed Java line.
"""
    # Call Ollama's chat API
    resp = ollama.chat(
        model=model,
        messages=[{'role':'user', 'content': prompt}]
    )
    # colored print of prompt and result
    print(f"\033[92m{prompt}\033[0m")
    # Extract generated text
    if isinstance(resp, dict) and 'message' in resp:
        content = resp['message']['content']
    else:
        content = resp.message.content
    transformed = content.strip()
    print(f"\033[94m{transformed}\033[0m")

    # Reapply original indentation
    line_out = indent + transformed
    # Ensure newline
    return line_out + ('\n' if not line_out.endswith('\n') else '')


def main():
    parser = argparse.ArgumentParser(
        description="Refactor Java Map calls to VO getters/setters using Ollama."
    )
    parser.add_argument('--input', '-i', required=True, help="Path to the original Java file.")
    parser.add_argument('--vo', '-v', required=True, help="Path to the Value Object Java file.")
    parser.add_argument('--output', '-o', required=True, help="Path to save the refactored file.")
    parser.add_argument(
        '--model', '-m', default='llama3.2',
        help="Ollama model to use (e.g., llama3.2, mistral)."
    )
    args = parser.parse_args()

    original = load_file(args.input)
    vo_def = load_file(args.vo)

    out_lines = []
    for line in original.splitlines(True):  # preserve newline in lines
        try:
            new_line = convert_line(line, vo_def, args.model)
        except Exception:
            new_line = line
        out_lines.append(new_line)

    write_file(args.output, ''.join(out_lines))
    print(f"Refactored file written to: {args.output}")


if __name__ == '__main__':
    main()
