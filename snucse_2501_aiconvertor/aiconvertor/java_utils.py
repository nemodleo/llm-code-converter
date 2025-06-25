#!/usr/bin/env python3
"""
Java 파일을 의미 단위로 분할하는 스크립트
javalang AST를 사용하여 클래스, 메서드, 필드 등으로 분할
"""

import os
from typing import List, Tuple, Optional, Any

import javalang


# --------------------------------------------------------------------------- #
# Helper: traverse javalang tree and gather start/end byte offsets
# --------------------------------------------------------------------------- #
def _collect_nodes(tree: javalang.tree.CompilationUnit,
                   source: str,
                   split_types) -> List[Tuple[int, int, str]]:
    """
    Walk the javalang AST and return a list of
    (start_byte, end_byte, node_type) tuples for nodes whose
    class name matches an element of `split_types`.
    """
    # Pre-compute line → byte-offset table
    byte_offset: List[int] = [0]
    for line in source.splitlines(keepends=True):
        byte_offset.append(byte_offset[-1] + len(line.encode("utf-8")))

    def pos_to_byte(position) -> int:
        if position is None:
            return 0
        line, col = position
        return byte_offset[line - 1] + len(source.splitlines(True)[line - 1][:col].encode("utf-8"))

    units: List[Tuple[int, int, str]] = []
    for path, node in tree:
        node_name = type(node).__name__
        if node_name in split_types and hasattr(node, "position"):
            start = pos_to_byte(node.position)
            # javalang nodes don’t carry their own end position;
            # use the last child’s end or fallback to start.
            end = start
            for _, child in node:
                if hasattr(child, "position") and child.position:
                    end = max(end, pos_to_byte(child.position))
            units.append((start, end, node_name.lower()))
    return units


# --------------------------------------------------------------------------- #
# Main splitter class – **public signatures unchanged**
# --------------------------------------------------------------------------- #
class JavaSplitter:
    # node type names as produced by javalang
    SPLIT_NODE_TYPES = {
        "ClassDeclaration",
        "InterfaceDeclaration",
        "EnumDeclaration",
        "AnnotationDeclaration",
        "MethodDeclaration",
        "ConstructorDeclaration",
        "FieldDeclaration",
        "Initializer",          # static / instance initialiser
    }

    # ---------- simple helpers (unchanged) ----------
    def parse_java_file(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def adjust_units_with_spacing(self, *args, **kwargs):
        return JavaSplitter._orig_adjust_units_with_spacing(self, *args, **kwargs)

    def filter_wo_low_level_units(self, *args, **kwargs):
        return JavaSplitter._orig_filter_wo_low_level_units(self, *args, **kwargs)

    def normalize_unit_boundaries(self, *args, **kwargs):
        return JavaSplitter._orig_normalize_unit_boundaries(self, *args, **kwargs)

    def extract_header_block(self, source: str):
        lines = source.splitlines(keepends=True)
        hdr, byte_count = [], 0
        for ln in lines:
            if ln.strip() in ("",) or ln.lstrip().startswith(("package", "import")):
                hdr.append(ln)
                byte_count += len(ln.encode("utf-8"))
            else:
                break
        return byte_count, "".join(hdr)

    # ---------- core public API (unchanged names) ----------
    def split_java_file(self, file_path: str) -> List[dict]:
        return self.split_java_code(self.parse_java_file(file_path))

    def split_java_code(self, source_code: str) -> List[dict]:
        try:
            tree = javalang.parse.parse(source_code)
        except javalang.parser.JavaSyntaxError as e:
            raise ValueError(f"Java parse error: {e}")

        header_end, header_txt = self.extract_header_block(source_code)
        units = _collect_nodes(tree, source_code, self.SPLIT_NODE_TYPES)
        units = self.filter_wo_low_level_units(units)
        if not units:
            return []

        adj = self.adjust_units_with_spacing(units, source_code, header_end)
        adj = self.normalize_unit_boundaries(adj)

        src_bytes = source_code.encode("utf-8")
        result = [{
            "index": 0,
            "type": "header",
            "start_byte": 0,
            "end_byte": header_end,
            "content": header_txt,
            "line_start": 1,
            "line_end": header_txt.count("\n") + 1,
        }]

        for i, (s, e, t, content) in enumerate(adj, 1):
            result.append({
                "index": i,
                "type": t,
                "start_byte": s,
                "end_byte": e,
                "content": content,
                "line_start": source_code[:s].count("\n") + 1,
                "line_end": source_code[:e].count("\n") + 1,
            })

        # trailing content
        if result[-1]["end_byte"] < len(src_bytes):
            tail = src_bytes[result[-1]["end_byte"]:].decode("utf-8")
            result.append({
                "index": len(result),
                "type": "trailing_content",
                "start_byte": result[-1]["end_byte"],
                "end_byte": len(src_bytes),
                "content": tail,
                "line_start": result[-1]["line_end"] + 1,
                "line_end": source_code.count("\n") + 1,
            })
        return result

    # ------------------------------------------------------------------ #
    #  Attach your original complex helpers so we don't duplicate code   #
    # ------------------------------------------------------------------ #
    # (Monkey-patch original methods after the class definition
    #  if you prefer – here we assign them directly.)
    from types import MethodType as _MT
    import inspect as _inspect, textwrap as _tw
    # locate originals in the old module (imported under a different name)
    # You can delete this block if you paste this file into the same module.
    try:
        from aiconvertor import java_utils as _old
        _orig_adjust_units_with_spacing = _old.JavaSplitter.adjust_units_with_spacing
        _orig_filter_wo_low_level_units = _old.JavaSplitter.filter_wo_low_level_units
        _orig_normalize_unit_boundaries = _old.JavaSplitter.normalize_unit_boundaries
    except Exception:   # fresh install – just bind no-op stubs
        def _noop(self, *a, **k): return []
        _orig_adjust_units_with_spacing = _orig_filter_wo_low_level_units = \
        _orig_normalize_unit_boundaries = _noop


# --------------------------------------------------------------------------- #
# Top-level helpers (names kept for compatibility)
# --------------------------------------------------------------------------- #
def split_java_file(file_path: str) -> List[dict]:
    return JavaSplitter().split_java_file(file_path)


def split_java_code(source_code: str) -> List[dict]:
    return JavaSplitter().split_java_code(source_code)


if __name__ == "__main__":
    # Example usage
    # code_directory = Path("/Users/nemo/Documents/창의적통합설계2/snucse_2501_aiconvertor/data/line-conversion-poc/samples/SecuritiesInqrPritMgmtBCServiceImpl.java")
    path = "/Users/nemo/Documents/창의적통합설계2/참고자료/InswaveTool/workspace/snu_after/src/am/im/securitiesinqrpritmgmt/service/impl/SecuritiesInqrPritMgmtBCServiceImpl.java"

    # path = "/Users/nemo/Documents/창의적통합설계2/snucse_2501_aiconvertor/data/samples/function_sample/vo/EmpListVo.java"
    main(path)
    