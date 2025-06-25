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

import argparse
import inspect
import os
import pathlib
import re
import sys
import textwrap
from typing import Dict, List

import ollama  # type: ignore – runtime dependency


def load_examples_txt(path: str) -> List[Dict[str, str]]:
    """Expect a plain‑text file where every example block looks like:
    Input: ....\nOutput: ....\n(blank line)"""
    examples: List[Dict[str, str]] = []
    current: Dict[str, str] = {}
    for line in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("Input:"):
            current["input"] = line[len("Input:"):].strip()
        elif line.startswith("Output:"):
            current["output"] = line[len("Output:"):].strip()
        elif not line.strip() and current:  # blank line ⇒ flush
            examples.append(current)
            current = {}
    if current:  # last one
        examples.append(current)
    return examples


def load_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def save_examples_txt(path: str, examples: List[Dict[str, str]]):
    with open(path, "w", encoding="utf-8") as f:
        for exp in examples:
            f.write(f"Input: {exp['input']}\n")
            f.write(f"Output: {exp['output']}\n\n")


if __name__ == "__main__":
    a, b = load_file("samples/SecuritiesInqrPritMgmtBCServiceImpl.java"), load_file("samples/gt.java")
    new_examples = []
    for line_a, line_b in zip(a.splitlines(), b.splitlines()):
        if line_a != line_b:
            new_examples.append({
                "input": line_a.strip(),
                "output": line_b.strip()
            })

    save_examples_txt("samples/in-context-examples-many.txt", new_examples)