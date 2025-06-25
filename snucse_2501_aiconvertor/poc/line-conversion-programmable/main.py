"""code_conversion_pipeline.py
A **self‑improving, colorful** pipeline with *example sampling*.

Work‑flow
---------
1.  Load full example list.
2.  Optionally pick a **random subset** (`--sample-size`) for the *first* LLM
    prompt.
3.  Generate `convert_line` via the LLM.
4.  Evaluate on **all** examples.
5.  If failures exist, feed **up to `--fail-sample-size`** failing cases back to
    the LLM, rewrite, and repeat (max `--max-iters`).
6.  Save final converter and rewrite target files.
"""
from __future__ import annotations

import argparse
import os
import pathlib
import random
import re
import sys
import textwrap
from typing import Dict, List

import ollama  # type: ignore

from llm_utils import Agent
from utils import load_examples_txt, load_file

_RESET = "\033[0m"; _BOLD = "\033[1m"; _CYAN = "\033[36m"; _GREEN = "\033[32m"; _YELLOW = "\033[33m"; _RED = "\033[31m"
_c = lambda t, c: f"{c}{t}{_RESET}"
_info = lambda m: print(_c(m, _CYAN), file=sys.stderr)
_ok   = lambda m: print(_c(m, _GREEN), file=sys.stderr)
_warn = lambda m: print(_c(m, _YELLOW), file=sys.stderr)
_err  = lambda m: print(_c(m, _RED), file=sys.stderr)

_BASE_PROMPT = textwrap.dedent("""
You are a senior Java tooling engineer.
Write a **single** Python function called `convert_line(line: str, vo_type: str = \"SecuritiesInqrPritMgmtVo\") -> str`.
The function must convert *one* line of legacy Map-based Java into its VO-style equivalent, exactly as shown in the examples.
Requirements:
  • Use only `re` (no 3rd-party deps).
  • Keep comments minimal.
  • Output *only* the function in one ```python``` block.
Examples:
{examples_block}
""")

_REFINE_PROMPT = textwrap.dedent("""
Your previous `convert_line` failed on these lines:
{failure_block}
Here is the current implementation:
```python
{current_function}
```
Rewrite the whole function so *all* of them pass.  Output only the new function in one ```python``` block.
""")

def _mk_block(ex: List[Dict[str, str]]) -> str:
    return "\n".join(f"Input: {e['input']}\nOutput: {e['output']}\n" for e in ex)


def _code_from_md(md: str) -> str:
    m = re.search(r"```python\s+(.*?)```", md, re.S)
    return m.group(1) if m else md


def _compile(code: str):
    ns: Dict[str, object] = {}
    exec(code, ns)
    fn = ns.get("convert_line")
    if not callable(fn):
        raise RuntimeError("convert_line not found")
    return fn


def _eval(fn, ex: List[Dict[str, str]], vo: str):
    fails = []
    for e in ex:
        try:
            got = fn(e["input"], vo_type=vo)
        except Exception as err:
            got = f"[ERROR] {type(err).__name__}: {err}"
        if got.strip() != e["output"].strip():
            fails.append({"input": e["input"], "expected": e["output"], "got": got})
    return fails


def main(argv: List[str] | None = None):
    p = argparse.ArgumentParser(description="Self‑improving converter with sampling")
    p.add_argument("files", nargs="+", help="Java files to rewrite")
    p.add_argument("--examples", default="samples/in-context-examples.txt")
    p.add_argument("--vo", default="SecuritiesInqrPritMgmtVo")
    p.add_argument("-m", "--model", default="llama3.2")
    p.add_argument("--suffix", default=".converted")
    p.add_argument("--save-converter", default="generated_converter.py")
    p.add_argument("--max-iters", type=int, default=3)
    p.add_argument("--sample-size", type=int, default=0)
    p.add_argument("--fail-sample-size", type=int, default=10)
    args = p.parse_args(argv)

    random.seed(0)
    ex_full = load_examples_txt(args.examples)
    if args.sample_size and args.sample_size < len(ex_full):
        ex_seed = random.sample(ex_full, args.sample_size)
        _info(f"Using random subset: {len(ex_seed)}/{len(ex_full)} examples")
    else:
        ex_seed = ex_full

    agent = Agent(model=args.model)
    prompt = _BASE_PROMPT.format(examples_block=_mk_block(ex_seed))
    md = agent(prompt)
    code = _code_from_md(md)
    _warn(_c(code, _YELLOW))
    fn = _compile(code)

    for itr in range(args.max_iters):
        fails = _eval(fn, ex_full, args.vo)
        if not fails:
            _ok(f"✓ All tests passed after {itr} iterations")
            break
        _warn(f"{len(fails)} failures (showing up to {args.fail_sample_size})")
        fails_sample = fails[: args.fail_sample_size]
        block = "\n".join(
            f"Input: {f['input']}\nExpected: {f['expected']}\nGot: {f['got']}\n" for f in fails_sample
        )
        _warn(block)
        refine_prompt = _REFINE_PROMPT.format(failure_block=block, current_function=code)
        md = agent(refine_prompt, clear_messages=False)
        code = _code_from_md(md)
        _warn(_c(code, _YELLOW))
        fn = _compile(code)
    else:
        _err("Max iterations reached without full pass")
        sys.exit(1)

    with open(args.save_converter, "w", encoding="utf-8") as f:
        f.write("# auto\n" + code + "\n")
    _ok(f"Saved converter to {args.save_converter}")

    for src_path in args.files:
        dst = pathlib.Path(src_path).with_suffix(pathlib.Path(src_path).suffix + args.suffix)
        _info(f"→ Converting {src_path} …")
        converted = [fn(line, vo_type=args.vo) for line in load_file(src_path).splitlines()]
        dst.write_text("\n".join(converted), encoding="utf-8")
        _ok(f"← Written {dst}")

if __name__ == "__main__":
    if os.name == "nt": os.system("")
    main()
