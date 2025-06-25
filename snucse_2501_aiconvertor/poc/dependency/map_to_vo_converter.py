#!/usr/bin/env python3
"""
Map<String, Object> to VO 변환기
프로젝트 내 모든 Map<String, Object> 사용을 분석하여 하나의 통합 VO로 변환
"""

import argparse
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Any
from dataclasses import dataclass, asdict
import shutil
from datetime import datetime

from .analyzer import ElementLevelDependencyAnalyzer


@dataclass
class MapKeyAnalysis:
    key: str
    value_types: Set[str]
    usage_count: int
    files: Set[str]
    operations: Set[str]
    line_examples: List[str]

@dataclass
class VOField:
    name: str
    java_type: str
    getter_name: str
    setter_name: str
    original_key: str

class MapToVOConverter:
    def __init__(self, project_root: str, vo_package: str = "com.example.vo", vo_class_name: str = "UnifiedDataVO"):
        self.project_root = Path(project_root)
        self.vo_package = vo_package
        self.vo_class_name = vo_class_name
        self.analyzer = ElementLevelDependencyAnalyzer(project_root, use_cache=True)
        
        # 분석 결과
        self.map_keys: Dict[str, MapKeyAnalysis] = {}
        self.map_variables: Set[str] = set()
        self.java_files: List[Path] = []
        self.vo_fields: List[VOField] = []
        
        # 백업 디렉토리
        self.backup_dir = self.project_root / f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
    def analyze_all_maps(self) -> Dict[str, Any]:
        """프로젝트 전체에서 Map 사용 패턴 분석"""
        print("=" * 60)
        print("1단계: Map 사용 패턴 분석")
        print("=" * 60)
        
        self.java_files = list(self.project_root.rglob("*.java"))
        print(f"분석할 Java 파일: {len(self.java_files)}개")
        
        for java_file in self.java_files:
            print(f"분석 중: {java_file.relative_to(self.project_root)}")
            self._analyze_file(java_file)
        
        self._generate_vo_structure()
        self._print_results()
        
        return self._create_report()
    
    def _analyze_file(self, file_path: Path):
        """개별 파일 분석"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Map 변수 찾기
            self._find_map_variables(content, str(file_path))
            
            # 키 사용 패턴 분석
            for i, line in enumerate(lines, 1):
                self._analyze_line(line, i, str(file_path))
                
        except Exception as e:
            print(f"  오류: {e}")
    
    def _find_map_variables(self, content: str, file_path: str):
        """Map 변수 선언 찾기"""
        patterns = [
            r'Map<\s*String\s*,\s*Object\s*>\s+(\w+)',
            r'Map\s+(\w+)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                var_name = match.group(1)
                self.map_variables.add(var_name)
                print(f"    Map 변수: {var_name}")
    
    def _analyze_line(self, line: str, line_num: int, file_path: str):
        """라인별 키 사용 패턴 분석"""
        original_line = line.strip()
        
        # get 패턴
        get_patterns = [
            r'(\w+)\.get\s*\(\s*["\']([^"\']+)["\']\s*\)',
            r'\.get\s*\(\s*["\']([^"\']+)["\']\s*\)',
        ]
        
        for pattern in get_patterns:
            matches = re.finditer(pattern, line)
            for match in matches:
                key = match.groups()[-1]
                self._record_key(key, "Object", "get", file_path, original_line)
        
        # put 패턴
        put_patterns = [
            r'(\w+)\.put\s*\(\s*["\']([^"\']+)["\']\s*,\s*(.+?)\)',
            r'\.put\s*\(\s*["\']([^"\']+)["\']\s*,\s*(.+?)\)',
        ]
        
        for pattern in put_patterns:
            matches = re.finditer(pattern, line)
            for match in matches:
                groups = match.groups()
                if len(groups) >= 2:
                    key = groups[-2]
                    value_expr = groups[-1]
                    value_type = self._infer_type(value_expr)
                    self._record_key(key, value_type, "put", file_path, original_line)
        
        # containsKey 패턴
        contains_patterns = [
            r'(\w+)\.containsKey\s*\(\s*["\']([^"\']+)["\']\s*\)',
            r'\.containsKey\s*\(\s*["\']([^"\']+)["\']\s*\)',
        ]
        
        for pattern in contains_patterns:
            matches = re.finditer(pattern, line)
            for match in matches:
                key = match.groups()[-1]
                self._record_key(key, "Object", "containsKey", file_path, original_line)
        
        # remove 패턴
        remove_patterns = [
            r'(\w+)\.remove\s*\(\s*["\']([^"\']+)["\']\s*\)',
            r'\.remove\s*\(\s*["\']([^"\']+)["\']\s*\)',
        ]
        
        for pattern in remove_patterns:
            matches = re.finditer(pattern, line)
            for match in matches:
                key = match.groups()[-1]
                self._record_key(key, "Object", "remove", file_path, original_line)
    
    def _record_key(self, key: str, value_type: str, operation: str, file_path: str, line_example: str):
        """키 사용 패턴 기록"""
        if not key or key.isspace():
            return
            
        if key not in self.map_keys:
            self.map_keys[key] = MapKeyAnalysis(
                key=key,
                value_types=set(),
                usage_count=0,
                files=set(),
                operations=set(),
                line_examples=[]
            )
        
        analysis = self.map_keys[key]
        analysis.value_types.add(value_type)
        analysis.usage_count += 1
        analysis.files.add(file_path)
        analysis.operations.add(operation)
        
        if len(analysis.line_examples) < 3:
            analysis.line_examples.append(line_example)
    
    def _infer_type(self, expr: str) -> str:
        """표현식에서 타입 추론"""
        if not expr:
            return "Object"
            
        expr = expr.strip()
        
        if expr.lower() == 'null':
            return "Object"
        
        if expr == 'true' or expr == 'false':
            return "Boolean"
        
        if re.match(r'^\d+$', expr):
            return "Integer"
        
        if re.match(r'^\d+L$', expr, re.IGNORECASE):
            return "Long"
        
        if re.match(r'^\d*\.\d+$', expr):
            return "Double"
        
        if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
            return "String"
        
        if expr.startswith('new '):
            if 'Date' in expr:
                return "Date"
            elif 'String' in expr:
                return "String"
            elif 'Integer' in expr:
                return "Integer"
        
        return "Object"
    
    def _generate_vo_structure(self):
        """VO 구조 생성"""
        print("\n" + "=" * 60)
        print("2단계: VO 구조 생성")
        print("=" * 60)
        
        sorted_keys = sorted(self.map_keys.items(), key=lambda x: x[1].usage_count, reverse=True)
        
        for key, analysis in sorted_keys:
            java_type = self._determine_type(analysis.value_types, key)
            field_name = self._to_field_name(key)
            
            # 중복 필드명 처리
            original_field_name = field_name
            counter = 1
            while any(f.name == field_name for f in self.vo_fields):
                field_name = f"{original_field_name}{counter}"
                counter += 1
            
            vo_field = VOField(
                name=field_name,
                java_type=java_type,
                getter_name=f"get{self._to_pascal_case(field_name)}",
                setter_name=f"set{self._to_pascal_case(field_name)}",
                original_key=key
            )
            
            self.vo_fields.append(vo_field)
            print(f"  필드: {field_name} ({java_type}) - 키: '{key}', 사용: {analysis.usage_count}회")
    
    def _to_field_name(self, key: str) -> str:
        """키를 필드명으로 변환"""
        if not key:
            return "unknownField"
        
        normalized = re.sub(r'[^\w]', '_', key)
        normalized = re.sub(r'_+', '_', normalized)
        normalized = normalized.strip('_')
        
        if '_' in normalized:
            return self._to_camel_case(normalized)
        
        return normalized if normalized else "unknownField"
    
    def _to_camel_case(self, snake_str: str) -> str:
        """snake_case를 camelCase로 변환"""
        if not snake_str:
            return "unknownField"
        components = snake_str.lower().split('_')
        return components[0] + ''.join(x.capitalize() for x in components[1:] if x)
    
    def _to_pascal_case(self, camel_str: str) -> str:
        """camelCase를 PascalCase로 변환"""
        if not camel_str:
            return "UnknownField"
        return camel_str[0].upper() + camel_str[1:]
    
    def _determine_type(self, value_types: Set[str], key: str) -> str:
        """타입 결정"""
        if not value_types:
            return self._guess_type_from_key(key)
        
        if "Object" in value_types and len(value_types) > 1:
            non_object_types = value_types - {"Object"}
            if len(non_object_types) == 1:
                return list(non_object_types)[0]
        
        if len(value_types) == 1:
            single_type = list(value_types)[0]
            if single_type == "Object":
                return self._guess_type_from_key(key)
            return single_type
        
        # 숫자 타입 우선순위
        for num_type in ["Double", "Float", "Long", "Integer"]:
            if num_type in value_types:
                return num_type
        
        if "Date" in value_types:
            return "Date"
        if "String" in value_types:
            return "String"
        if "Boolean" in value_types:
            return "Boolean"
        
        return "Object"
    
    def _guess_type_from_key(self, key: str) -> str:
        """키 이름으로 타입 추정"""
        if not key:
            return "Object"
        
        key_lower = key.lower()
        
        if 'id' in key_lower:
            return "String"
        
        if any(pattern in key_lower for pattern in ['count', 'num', 'size', 'age']):
            return "Integer"
        
        if any(pattern in key_lower for pattern in ['amount', 'price', 'salary', 'rate']):
            return "Double"
        
        if any(pattern in key_lower for pattern in ['date', 'time', 'created', 'updated']):
            return "Date"
        
        if any(pattern in key_lower for pattern in ['is_', 'has_', 'active', 'flag']):
            return "Boolean"
        
        return "String"
    
    def _print_results(self):
        """분석 결과 출력"""
        print("\n" + "=" * 60)
        print("분석 결과")
        print("=" * 60)
        print(f"Java 파일: {len(self.java_files)}개")
        print(f"Map 변수: {len(self.map_variables)}개")
        print(f"고유 키: {len(self.map_keys)}개")
        print(f"VO 필드: {len(self.vo_fields)}개")
        
        if self.map_variables:
            print(f"\nMap 변수들: {', '.join(sorted(self.map_variables))}")
        
        print("\n키별 상세 정보 (상위 10개):")
        sorted_keys = sorted(self.map_keys.items(), key=lambda x: x[1].usage_count, reverse=True)
        for key, analysis in sorted_keys[:10]:
            print(f"  '{key}': {analysis.usage_count}회 사용")
            print(f"    타입: {list(analysis.value_types)}")
            if analysis.line_examples:
                print(f"    예시: {analysis.line_examples[0]}")
    
    def generate_vo_class(self) -> str:
        """VO 클래스 코드 생성"""
        print("\n" + "=" * 60)
        print("3단계: VO 클래스 생성")
        print("=" * 60)
        
        code = f"""package {self.vo_package};

import java.util.*;
import java.sql.Timestamp;

/**
 * 통합 데이터 전달 객체
 * 자동 생성일: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
 * 필드 수: {len(self.vo_fields)}개
 */
public class {self.vo_class_name} {{

"""
        
        # 필드 선언
        for field in self.vo_fields:
            code += f"    /** 원본 키: '{field.original_key}' */\n"
            code += f"    private {field.java_type} {field.name};\n\n"
        
        # 기본 생성자
        code += f"    public {self.vo_class_name}() {{}}\n\n"
        
        # Map 생성자
        code += f"    public {self.vo_class_name}(Map<String, Object> map) {{\n"
        code += f"        fromMap(map);\n"
        code += f"    }}\n\n"
        
        # Getter/Setter
        for field in self.vo_fields:
            # Getter
            code += f"    public {field.java_type} {field.getter_name}() {{\n"
            code += f"        return {field.name};\n"
            code += f"    }}\n\n"
            
            # Setter
            code += f"    public void {field.setter_name}({field.java_type} {field.name}) {{\n"
            code += f"        this.{field.name} = {field.name};\n"
            code += f"    }}\n\n"
        
        # Map 변환 메서드
        code += self._generate_conversion_methods()
        
        # 유틸리티 메서드
        code += self._generate_utility_methods()
        
        code += "}\n"
        
        return code
    
    def _generate_conversion_methods(self) -> str:
        """Map 변환 메서드 생성"""
        code = f"""    // Map에서 VO로 변환
    public void fromMap(Map<String, Object> map) {{
        if (map == null) return;
        
"""
        
        for field in self.vo_fields:
            code += f'        Object {field.name}Value = map.get("{field.original_key}");\n'
            code += f'        if ({field.name}Value != null) {{\n'
            
            if field.java_type == "String":
                code += f'            this.{field.name} = {field.name}Value.toString();\n'
            elif field.java_type == "Integer":
                code += f'            if ({field.name}Value instanceof Integer) {{\n'
                code += f'                this.{field.name} = (Integer) {field.name}Value;\n'
                code += f'            }} else {{\n'
                code += f'                try {{ this.{field.name} = Integer.valueOf({field.name}Value.toString()); }} catch (Exception e) {{ }}\n'
                code += f'            }}\n'
            elif field.java_type == "Long":
                code += f'            if ({field.name}Value instanceof Long) {{\n'
                code += f'                this.{field.name} = (Long) {field.name}Value;\n'
                code += f'            }} else if ({field.name}Value instanceof Integer) {{\n'
                code += f'                this.{field.name} = ((Integer) {field.name}Value).longValue();\n'
                code += f'            }} else {{\n'
                code += f'                try {{ this.{field.name} = Long.valueOf({field.name}Value.toString()); }} catch (Exception e) {{ }}\n'
                code += f'            }}\n'
            elif field.java_type == "Double":
                code += f'            if ({field.name}Value instanceof Double) {{\n'
                code += f'                this.{field.name} = (Double) {field.name}Value;\n'
                code += f'            }} else if ({field.name}Value instanceof Number) {{\n'
                code += f'                this.{field.name} = ((Number) {field.name}Value).doubleValue();\n'
                code += f'            }} else {{\n'
                code += f'                try {{ this.{field.name} = Double.valueOf({field.name}Value.toString()); }} catch (Exception e) {{ }}\n'
                code += f'            }}\n'
            elif field.java_type == "Boolean":
                code += f'            if ({field.name}Value instanceof Boolean) {{\n'
                code += f'                this.{field.name} = (Boolean) {field.name}Value;\n'
                code += f'            }} else {{\n'
                code += f'                this.{field.name} = Boolean.valueOf({field.name}Value.toString());\n'
                code += f'            }}\n'
            elif field.java_type == "Date":
                code += f'            if ({field.name}Value instanceof Date) {{\n'
                code += f'                this.{field.name} = (Date) {field.name}Value;\n'
                code += f'            }} else if ({field.name}Value instanceof Timestamp) {{\n'
                code += f'                this.{field.name} = new Date(((Timestamp) {field.name}Value).getTime());\n'
                code += f'            }} else if ({field.name}Value instanceof Long) {{\n'
                code += f'                this.{field.name} = new Date((Long) {field.name}Value);\n'
                code += f'            }}\n'
            else:
                code += f'            this.{field.name} = ({field.java_type}) {field.name}Value;\n'
            
            code += f'        }}\n\n'
        
        code += f"""    }}

    // VO에서 Map으로 변환
    public Map<String, Object> toMap() {{
        Map<String, Object> map = new HashMap<>();
"""
        
        for field in self.vo_fields:
            code += f'        if (this.{field.name} != null) {{\n'
            code += f'            map.put("{field.original_key}", this.{field.name});\n'
            code += f'        }}\n'
        
        code += f"""        return map;
    }}

    // 정적 변환 메서드
    public static {self.vo_class_name} fromMap(Map<String, Object> map) {{
        if (map == null) return null;
        return new {self.vo_class_name}(map);
    }}

"""
        return code
    
    def _generate_utility_methods(self) -> str:
        """유틸리티 메서드 생성"""
        code = f"""    // 특정 키 값 존재 확인
    public boolean hasValue(String key) {{
        switch (key) {{
"""
        
        for field in self.vo_fields:
            code += f'            case "{field.original_key}": return this.{field.name} != null;\n'
        
        code += f"""            default: return false;
        }}
    }}

    // 특정 키 값 조회
    public Object getValue(String key) {{
        switch (key) {{
"""
        
        for field in self.vo_fields:
            code += f'            case "{field.original_key}": return this.{field.name};\n'
        
        code += f"""            default: return null;
        }}
    }}

    @Override
    public String toString() {{
        return "{self.vo_class_name}{{" +
"""
        
        for i, field in enumerate(self.vo_fields[:5]):  # 처음 5개만
            if i == 0:
                code += f'                "{field.name}=" + {field.name} +\n'
            else:
                code += f'                ", {field.name}=" + {field.name} +\n'
        
        if len(self.vo_fields) > 5:
            code += f'                ", ..." +\n'
        
        code += f"""                '}}';
    }}

    @Override
    public boolean equals(Object o) {{
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        {self.vo_class_name} that = ({self.vo_class_name}) o;
        return Objects.equals({self.vo_fields[0].name if self.vo_fields else 'null'}, that.{self.vo_fields[0].name if self.vo_fields else 'null'});
    }}

    @Override
    public int hashCode() {{
        return Objects.hash({self.vo_fields[0].name if self.vo_fields else 'null'});
    }}
"""
        return code
    
    def create_backup(self):
        """백업 생성"""
        print("\n" + "=" * 60)
        print("4단계: 백업 생성")
        print("=" * 60)
        
        self.backup_dir.mkdir(exist_ok=True)
        
        for java_file in self.java_files:
            relative_path = java_file.relative_to(self.project_root)
            backup_file = self.backup_dir / relative_path
            backup_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(java_file, backup_file)
        
        print(f"백업 완료: {self.backup_dir}")
    
    def convert_all_files(self):
        """모든 파일 변환"""
        print("\n" + "=" * 60)
        print("5단계: 파일 변환")
        print("=" * 60)
        
        converted = 0
        
        for java_file in self.java_files:
            if self._convert_file(java_file):
                converted += 1
        
        print(f"\n변환 완료: {converted}개 파일")
    
    def _convert_file(self, file_path: Path) -> bool:
        """개별 파일 변환"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # Import 추가
            content = self._add_import(content)
            
            # Map 선언 변경
            content = self._convert_declarations(content)
            
            # Map 연산 변경
            content = self._convert_operations(content)
            
            if content != original:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  변환: {file_path.relative_to(self.project_root)}")
                return True
            
            return False
            
        except Exception as e:
            print(f"변환 오류 {file_path}: {e}")
            return False
    
    def _add_import(self, content: str) -> str:
        """Import 추가"""
        vo_import = f"import {self.vo_package}.{self.vo_class_name};"
        
        if vo_import not in content:
            package_pattern = r'(package\s+[^;]+;)'
            if re.search(package_pattern, content):
                content = re.sub(package_pattern, r'\1\n' + vo_import, content)
            else:
                content = vo_import + "\n\n" + content
        
        return content
    
    def _convert_declarations(self, content: str) -> str:
        """Map 선언 변경"""
        patterns = [
            (r'Map<\s*String\s*,\s*Object\s*>', self.vo_class_name),
            (r'List<\s*Map<\s*String\s*,\s*Object\s*>\s*>', f'List<{self.vo_class_name}>'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        # new HashMap 변경
        content = re.sub(r'new\s+HashMap<[^>]*>\s*\(\)', f'new {self.vo_class_name}()', content, flags=re.IGNORECASE)
        content = re.sub(r'new\s+HashMap\s*\(\)', f'new {self.vo_class_name}()', content, flags=re.IGNORECASE)
        
        return content
    
    def _convert_operations(self, content: str) -> str:
        """Map 연산 변경"""
        for field in self.vo_fields:
            key = field.original_key
            
            # get 변환
            content = re.sub(rf'(\w+)\.get\s*\(\s*["\']({re.escape(key)})["\']\s*\)', 
                           rf'\1.{field.getter_name}()', content)
            content = re.sub(rf'\.get\s*\(\s*["\']({re.escape(key)})["\']\s*\)', 
                           rf'.{field.getter_name}()', content)
            
            # put 변환
            content = re.sub(rf'(\w+)\.put\s*\(\s*["\']({re.escape(key)})["\']\s*,\s*(.+?)\)', 
                           rf'\1.{field.setter_name}(\3)', content)
            content = re.sub(rf'\.put\s*\(\s*["\']({re.escape(key)})["\']\s*,\s*(.+?)\)', 
                           rf'.{field.setter_name}(\2)', content)
            
            # containsKey 변환
            content = re.sub(rf'(\w+)\.containsKey\s*\(\s*["\']({re.escape(key)})["\']\s*\)', 
                           rf'\1.hasValue("{key}")', content)
            
            # remove 변환
            content = re.sub(rf'(\w+)\.remove\s*\(\s*["\']({re.escape(key)})["\']\s*\)', 
                           rf'\1.{field.setter_name}(null)', content)
        
        return content
    
    def save_vo_class(self):
        """VO 클래스 파일 저장"""
        print("\n" + "=" * 60)
        print("6단계: VO 클래스 저장")
        print("=" * 60)
        
        # 패키지 디렉토리 생성
        vo_path = self.project_root / "src" / "main" / "java"
        for part in self.vo_package.split('.'):
            vo_path = vo_path / part
        
        vo_path.mkdir(parents=True, exist_ok=True)
        
        # 클래스 파일 생성
        vo_file = vo_path / f"{self.vo_class_name}.java"
        vo_code = self.generate_vo_class()
        
        with open(vo_file, 'w', encoding='utf-8') as f:
            f.write(vo_code)
        
        print(f"VO 클래스 생성: {vo_file}")
        return vo_file
    
    def _create_report(self) -> Dict[str, Any]:
        """분석 보고서 생성"""
        return {
            'timestamp': datetime.now().isoformat(),
            'project_root': str(self.project_root),
            'vo_class_name': self.vo_class_name,
            'vo_package': self.vo_package,
            'statistics': {
                'java_files': len(self.java_files),
                'map_variables': len(self.map_variables),
                'unique_keys': len(self.map_keys),
                'vo_fields': len(self.vo_fields)
            },
            'map_variables': list(self.map_variables),
            'map_keys': {
                key: {
                    'usage_count': analysis.usage_count,
                    'value_types': list(analysis.value_types),
                    'operations': list(analysis.operations),
                    'files_count': len(analysis.files),
                    'examples': analysis.line_examples
                }
                for key, analysis in self.map_keys.items()
            },
            'vo_fields': [asdict(field) for field in self.vo_fields],
            'backup_directory': str(self.backup_dir)
        }
    
    def generate_summary_report(self) -> str:
        """요약 보고서 생성"""
        sorted_fields = sorted(self.vo_fields, 
                             key=lambda f: self.map_keys.get(f.original_key, 
                                                           MapKeyAnalysis('', set(), 0, set(), set(), [])).usage_count, 
                             reverse=True)
        
        report = f"""
Map to VO 변환 보고서
{'=' * 50}
변환 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
프로젝트: {self.project_root}

변환 통계:
- Java 파일: {len(self.java_files)}개
- Map 변수: {len(self.map_variables)}개
- 고유 키: {len(self.map_keys)}개
- VO 필드: {len(self.vo_fields)}개

생성된 VO:
- 클래스명: {self.vo_class_name}
- 패키지: {self.vo_package}

주요 필드 (사용빈도순):
"""
        
        for field in sorted_fields[:15]:
            key_info = self.map_keys.get(field.original_key, 
                                       MapKeyAnalysis('', set(), 0, set(), set(), []))
            report += f"- {field.name} ({field.java_type}) - 키: '{field.original_key}', 사용: {key_info.usage_count}회\n"
        
        if len(sorted_fields) > 15:
            report += f"... 그 외 {len(sorted_fields) - 15}개 필드\n"
        
        report += f"""
변환 규칙:
1. Map<String, Object> → {self.vo_class_name}
2. new HashMap<>() → new {self.vo_class_name}()
3. map.get("key") → vo.getField()
4. map.put("key", value) → vo.setField(value)
5. map.containsKey("key") → vo.hasValue("key")
6. map.remove("key") → vo.setField(null)

주의사항:
- 백업 생성됨: {self.backup_dir}
- 변환 후 컴파일 및 테스트 필요
"""
        return report


def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description='Map<String, Object>을 VO로 변환')
    parser.add_argument('project_root', help='Java 프로젝트 루트 디렉토리')
    parser.add_argument('--vo-package', default='com.example.vo', help='VO 패키지명')
    parser.add_argument('--vo-class', default='UnifiedDataVO', help='VO 클래스명')
    parser.add_argument('--dry-run', action='store_true', help='분석만 수행')
    parser.add_argument('--report-file', help='보고서 파일명')
    parser.add_argument('--no-backup', action='store_true', help='백업 생성 안함')
    
    args = parser.parse_args()
    
    try:
        print("Map<String, Object> to VO 변환 도구")
        print("=" * 50)
        
        # 변환기 초기화
        converter = MapToVOConverter(
            project_root=args.project_root,
            vo_package=args.vo_package,
            vo_class_name=args.vo_class
        )
        
        # 분석 수행
        report = converter.analyze_all_maps()
        
        if not converter.map_keys:
            print("\n❌ Map<String, Object> 사용을 찾을 수 없습니다.")
            return 1
        
        # dry-run 모드
        if args.dry_run:
            print("\n🔍 DRY RUN 모드 - 분석만 수행")
            print(converter.generate_summary_report())
            
            if args.report_file:
                with open(args.report_file, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
                print(f"\n📄 보고서 저장: {args.report_file}")
            
            return 0
        
        # 사용자 확인
        print(f"\n⚠️  변환 작업:")
        print(f"- {len(converter.java_files)}개 파일 처리")
        print(f"- {len(converter.map_keys)}개 키 → {len(converter.vo_fields)}개 필드")
        print(f"- VO 생성: {args.vo_package}.{args.vo_class}")
        
        if not args.no_backup:
            print(f"- 백업 생성")
        
        confirm = input("\n계속하시겠습니까? (y/N): ")
        if confirm.lower() != 'y':
            print("❌ 취소됨")
            return 0
        
        # 백업 생성
        if not args.no_backup:
            converter.create_backup()
        
        # VO 클래스 생성
        converter.save_vo_class()
        
        # 파일 변환
        converter.convert_all_files()
        
        # 완료 보고서
        print("\n" + "=" * 50)
        print("✅ 변환 완료!")
        print("=" * 50)
        print(converter.generate_summary_report())
        
        # 보고서 저장
        if args.report_file:
            with open(args.report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\n📄 상세 보고서: {args.report_file}")
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())


# 사용 예시:
# poetry run python map_to_vo_converter.py ./sample-project --dry-run
# poetry run python map_to_vo_converter.py ./sample-project --vo-class DataVO