#!/usr/bin/env python3
"""
Java 파일을 의미 단위로 분할하는 스크립트
tree-sitter-java를 사용하여 클래스, 메서드, 필드 등으로 분할
"""

import sys
import os
from typing import List, Tuple, Optional
import tree_sitter_java
from tree_sitter import Language, Parser, Node

class JavaSplitter:
    def __init__(self):
        # Java 언어 설정
        self.java_language = Language(tree_sitter_java.language(), "java")
        self.parser = Parser()
        self.parser.set_language(self.java_language)

        # 분할할 의미 단위 노드 타입들
        self.SPLIT_NODE_TYPES = {
            'class_declaration',
            'interface_declaration',
            'enum_declaration',
            'annotation_type_declaration',
            'method_declaration',
            'constructor_declaration',
            'field_declaration',
            'static_initializer',
            'instance_initializer'
        }
    
    def parse_java_file(self, file_path: str) -> str:
        """Java 파일을 읽고 파싱"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            raise Exception(f"파일 읽기 실패: {e}")
    
    def get_meaningful_units(self, root_node: Node, source_code: bytes) -> List[Tuple[int, int, str]]:
        """의미 있는 단위들을 추출"""
        units = []
        
        def traverse(node: Node):
            # 현재 노드가 분할 대상인지 확인
            if node.type in self.SPLIT_NODE_TYPES:
                start_byte = node.start_byte
                end_byte = node.end_byte
                node_type = node.type
                units.append((start_byte, end_byte, node_type))
            
            # 자식 노드들을 재귀적으로 탐색
            for child in node.children:
                traverse(child)
        
        traverse(root_node)
        
        # 시작 위치순으로 정렬
        units.sort(key=lambda x: x[0])
        return units
    
    def adjust_units_with_spacing(self, units: List[Tuple[int, int, str]], 
                                 source_code: str,
                                 min_start: int = 0) -> List[Tuple[int, int, str, str]]:
        """단위 사이의 공백과 주석을 다음 단위에 포함"""
        if not units:
            return []
        
        adjusted_units = []
        source_bytes = source_code.encode('utf-8')
        
        for i, (start_byte, end_byte, node_type) in enumerate(units):
            # 첫 번째 단위가 아닌 경우, 이전 단위의 끝부터 현재 단위 시작까지의 내용을 포함
            if i > 0:
                prev_end = units[i-1][1]
                # 이전 단위 끝부터 현재 단위 시작까지의 공백/주석을 현재 단위에 포함
                actual_start = prev_end
            else:
                # 첫 번째 단위는 파일 시작부터
                # 첫 단위의 시작은 헤더 끝 이후부터
                actual_start = min_start
            actual_start = max(actual_start, min_start)  # 중복 방지
            
            # 현재 단위의 내용 추출
            unit_content = source_bytes[actual_start:end_byte].decode('utf-8')
            
            adjusted_units.append((actual_start, end_byte, node_type, unit_content))
        
        return adjusted_units

    def filter_top_level_units(self, units: List[Tuple[int, int, str]]) -> List[Tuple[int, int, str]]:
        """
        다른 유닛의 범위에 포함된 (즉, 중첩된) 유닛을 제거하여
        최상위 레벨의 의미 단위만 반환한다.
        
        units: (start_byte, end_byte, node_type) 튜플들의 리스트
        """
        filtered = []
        for i, (start_i, end_i, _) in enumerate(units):
            is_nested = False
            for j, (start_j, end_j, _) in enumerate(units):
                if i == j:
                    continue
                # 자신보다 바깥 범위에 포함된 경우 → 내부 유닛
                if start_j <= start_i and end_i <= end_j:
                    is_nested = True
                    break
            if not is_nested:
                filtered.append(units[i])
        return filtered
        
    def filter_wo_low_level_units(self, units: List[Tuple[int, int, str]]) -> List[Tuple[int, int, str]]:
        # ✅ 가장 짧은 단위를 먼저 처리
        units = sorted(units, key=lambda x: (x[1] - x[0], x[0]))

        occupied: List[Tuple[int, int]] = []
        result: List[Tuple[int, int, str]] = []

        def subtract_ranges(start: int, end: int, blocks: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
            remaining = []
            cursor = start
            for b_start, b_end in sorted(blocks):
                if b_end <= cursor:
                    continue
                if b_start >= end:
                    break
                if cursor < b_start:
                    remaining.append((cursor, b_start))
                cursor = max(cursor, b_end)
            if cursor < end:
                remaining.append((cursor, end))
            return remaining

        for start, end, node_type in units:
            # print(f"\n🔍 처리중: {node_type}: {start} ~ {end}")
            remaining_parts = subtract_ranges(start, end, occupied)

            if not remaining_parts:
                # print(f"⚠️  전체가 이미 점유됨: {node_type} {start} ~ {end}")
                continue

            for s, e in remaining_parts:
                # print(f"✅ 남은 조각: {s} ~ {e} ({node_type})")
                result.append((s, e, node_type))
                occupied.append((s, e))

            # print(f"📌 점유 상태: {sorted(occupied)}")

        return sorted(result)
    
    def extract_header_block(self, source_code: str) -> Tuple[int, str]:
        """package, import 블록을 추출"""
        lines = source_code.splitlines(keepends=True)
        header_lines = []
        end_byte = 0

        for line in lines:
            if line.strip().startswith("package") or line.strip().startswith("import") or line.strip() == "":
                header_lines.append(line)
                end_byte += len(line.encode('utf-8'))
            else:
                break

        return end_byte, ''.join(header_lines)

    def is_blank_or_comment_only(self, content: str) -> bool:
        """
        유닛 내용이 공백 또는 주석만으로 이루어졌는지 확인
        """
        lines = content.strip().splitlines()
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if not (stripped.startswith("//") or stripped.startswith("/*") or stripped.endswith("*/")):
                return False
        return True


    def normalize_unit_boundaries(self, adjusted_units: List[Tuple[int, int, str, str]]) -> List[Tuple[int, int, str, str]]:
        """
        유닛들의 trailing whitespace/comment 를 다음 유닛의 앞쪽으로 넘긴다.
        넘겨서 빈 문자열이 된 유닛은 삭제한다.
        """
        if not adjusted_units:
            return []
        
        # 작업용 리스트 생성 (원본 수정 방지)
        working_units = list(adjusted_units)
        normalized = []
        i = 0
        
        while i < len(working_units):
            start_byte, end_byte, node_type, content = working_units[i]
            
            # 마지막 유닛이 아닌 경우, trailing whitespace/comment를 다음 유닛으로 이동
            if i < len(working_units) - 1:
                # 현재 유닛의 content에서 trailing whitespace/comment 찾기
                lines = content.splitlines(keepends=True)
                
                # 뒤에서부터 공백이나 주석 라인 찾기
                trailing_start_idx = len(lines)
                for j in range(len(lines) - 1, -1, -1):
                    line = lines[j]
                    stripped = line.strip()
                    
                    # 공백 라인이거나 주석 라인인 경우
                    if (not stripped or 
                        stripped.startswith("//") or 
                        stripped.startswith("/*") or 
                        stripped.endswith("*/") or
                        stripped.startswith("*")):
                        trailing_start_idx = j
                    else:
                        break
                
                # trailing 부분이 있는 경우
                if trailing_start_idx < len(lines):
                    # 현재 유닛에서 trailing 부분 제거
                    main_content = ''.join(lines[:trailing_start_idx])
                    trailing_content = ''.join(lines[trailing_start_idx:])
                    
                    # main_content가 빈 문자열이거나 공백만 있는 경우
                    if main_content.strip():
                        # 바이트 위치 계산
                        main_content_bytes = len(main_content.encode('utf-8'))
                        new_end_byte = start_byte + main_content_bytes
                        
                        # 현재 유닛 추가
                        normalized.append((start_byte, new_end_byte, node_type, main_content))
                        
                        # 다음 유닛 업데이트
                        next_start, next_end, next_type, next_content = working_units[i + 1]
                        combined_content = trailing_content + next_content
                        working_units[i + 1] = (start_byte + main_content_bytes, next_end, next_type, combined_content)
                    else:
                        # 현재 유닛이 비어있으므로 삭제하고, 전체 content를 다음 유닛에 추가
                        next_start, next_end, next_type, next_content = working_units[i + 1]
                        combined_content = content + next_content
                        working_units[i + 1] = (start_byte, next_end, next_type, combined_content)
                        # 현재 유닛은 normalized에 추가하지 않음 (삭제)
                else:
                    # trailing 부분이 없는 경우, 현재 유닛이 공백만 있는지 확인
                    if content.strip():
                        # 내용이 있으면 그대로 추가
                        normalized.append((start_byte, end_byte, node_type, content))
                    else:
                        # 현재 유닛이 공백만 있으므로 다음 유닛에 병합
                        next_start, next_end, next_type, next_content = working_units[i + 1]
                        combined_content = content + next_content
                        working_units[i + 1] = (start_byte, next_end, next_type, combined_content)
                        # 현재 유닛은 normalized에 추가하지 않음 (삭제)
            else:
                # 마지막 유닛 처리
                if content.strip():
                    # 내용이 있으면 추가
                    normalized.append((start_byte, end_byte, node_type, content))
                # 마지막 유닛이 빈 문자열이면 삭제 (추가하지 않음)
            
            i += 1
        
        return normalized

    def split_java_file(self, file_path: str) -> List[dict]:
        source_code = self.parse_java_file(file_path)
        return self.split_java_code(source_code)

    def split_java_code(self, source_code: str) -> List[dict]:
        """Java 파일을 의미 단위로 분할"""
        # 파일 읽기
        source_bytes = source_code.encode('utf-8')
        
        # 파싱
        tree = self.parser.parse(source_bytes)
        root_node = tree.root_node

        # 헤더 블록 추출
        header_end_byte, header_content = self.extract_header_block(source_code)
        
        # 의미 단위 추출
        units = self.get_meaningful_units(root_node, source_bytes)

        # 최상위 레벨 유닛 필터링
        # units = self.filter_top_level_units(units)
        units = self.filter_wo_low_level_units(units)

        if not units:
            print("분할할 의미 단위를 찾을 수 없습니다.")
            return []
        
        
        # 공백/주석 포함하여 단위 조정
        adjusted_units = self.adjust_units_with_spacing(units, source_code, min_start=header_end_byte)

        # 공백-only 유닛 병합 등 경계 정규화
        adjusted_units = self.normalize_unit_boundaries(adjusted_units)

        # 결과 정리
        result = []

        result.append({
            'index': 0,
            'type': 'header',
            'start_byte': 0,
            'end_byte': header_end_byte,
            'content': header_content,
            'line_start': 1,
            'line_end': header_content.count('\n') + 1
        })

        for i, (start_byte, end_byte, node_type, content) in enumerate(adjusted_units):
            result.append({
                'index': i + 1,
                'type': node_type,
                'start_byte': start_byte,
                'end_byte': end_byte,
                'content': content,
                'line_start': source_code[:start_byte].count('\n') + 1,
                'line_end': source_code[:end_byte].count('\n') + 1
            })

        if result[-1]['end_byte'] < len(source_bytes):
            trailing_content = source_bytes[result[-1]['end_byte']:].decode('utf-8')
            # if trailing_content.strip():
            result.append({
                'index': len(result),
                'type': 'trailing_content',
                'start_byte': result[-1]['end_byte'],
                'end_byte': len(source_bytes),
                'content': trailing_content,
                'line_start': result[-1]['line_end'] + 1,
                'line_end': source_code.count('\n') + 1
            })
        
        return result
    
    def save_split_units(self, units: List[dict], output_dir: str, base_filename: str):
        """분할된 단위들을 별도 파일로 저장"""
        os.makedirs(output_dir, exist_ok=True)
        
        for unit in units:
            filename = f"{base_filename}_{unit['index']:03d}_{unit['type']}.java"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(unit['content'])
            
            print(f"저장됨: {filepath} (라인 {unit['line_start']}-{unit['line_end']})")

    def save_split_units_one_file(self, units: List[dict], output_path: str, original_path: str):
        """
        모든 유닛을 하나의 파일로 저장하고 원본 파일과 동일한지 확인
        """
        # 유닛 순서대로 content 병합
        merged_content = ''.join(unit['content'] for unit in units)
        
        # 병합된 내용을 저장
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(merged_content)
        
        print(f"\n모든 유닛이 병합되어 저장됨: {output_path}")
        
        # 원본과 비교
        with open(original_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        if merged_content == original_content:
            print("✅ 병합된 결과가 원본 파일과 정확히 일치합니다.")
        else:
            print("❌ 병합된 결과가 원본 파일과 다릅니다.")
            # 선택적으로 차이 출력
            import difflib
            diff = difflib.unified_diff(
                original_content.splitlines(),
                merged_content.splitlines(),
                fromfile='original',
                tofile='merged',
                lineterm=''
            )
            print("\n".join(list(diff)[:20]) + "\n... (이후 생략)")  # 처음 몇 줄만 출력


def split_java_file(file_path: str) -> List[dict]:
    """Java 파일을 의미 단위로 분할하는 함수"""
    splitter = JavaSplitter()
    return splitter.split_java_file(file_path)


def split_java_code(source_code: str) -> List[dict]:
    """Java 코드를 의미 단위로 분할하는 함수"""
    splitter = JavaSplitter()
    return splitter.split_java_code(source_code)


def matches_regardless_of_spacing(a: str, b: str) -> bool:
    """
    공백을 무시하고 두 문자열이 같은지 비교합니다.
    
    Args:
        a, b: 비교할 문자열들
        
    Returns:
        공백 제거 후 동일 여부
    """
    return ''.join(a.split()) == ''.join(b.split())


def get_ast(java_code: str) -> Node:
    """Java 코드를 AST로 변환"""
    java_language = Language(tree_sitter_java.language(), "java")
    parser = Parser()
    parser.set_language(java_language)
    java_bytes = java_code.encode('utf-8')
    tree = parser.parse(java_bytes)

    return tree.root_node


def main(java_file_path):
    splitter = JavaSplitter()
    
    print(f"Java 파일 분석 중: {java_file_path}")
    units = splitter.split_java_file(java_file_path)
    
    if not units:
        print("분할할 단위를 찾을 수 없습니다.")
        return
    
    # 결과 출력
    print(f"\n총 {len(units)}개의 의미 단위를 찾았습니다:")
    print("-" * 80)
    
    for unit in units:
        print(f"[{unit['index']}] {unit['type']}")
        print(f"  라인: {unit['line_start']}-{unit['line_end']}")
        print(f"  바이트: {unit['start_byte']}-{unit['end_byte']}")
        print(f"  크기: {len(unit['content'])} 문자")
        
        # 내용 미리보기 (첫 3줄)
        preview_lines = unit['content'].strip().split('\n')[:3]
        for line in preview_lines:
            print(f"  | {line}")
        if len(unit['content'].strip().split('\n')) > 3:
            print(f"  | ... (총 {len(unit['content'].strip().split('\n'))}줄)")
        print()


    # 단위들을 하나의 파일로 저장
    print("모든 단위를 하나의 파일로 저장합니다...")
    splitter.save_split_units_one_file(units, f"test.java", java_file_path)
    
    # 파일로 저장할지 묻기
    save_choice = input("분할된 단위들을 별도 파일로 저장하시겠습니까? (y/N): ").strip().lower()
    
    if save_choice == 'y':
        base_name = os.path.splitext(os.path.basename(java_file_path))[0]
        output_dir = f"{base_name}_split"
        
        splitter.save_split_units(units, output_dir, base_name)
        print(f"\n모든 단위가 '{output_dir}' 디렉토리에 저장되었습니다.")
