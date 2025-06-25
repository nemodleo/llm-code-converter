import argparse
import tree_sitter_java
import json

from pathlib import Path
from collections import defaultdict
from typing import Any
from tree_sitter import Language, Parser
from dataclasses import dataclass, asdict


@dataclass
class CodeElement:
    """코드 요소 정보"""
    name: str
    type: str  # 'class', 'method', 'field', 'constructor', 'enum', 'interface'
    line_start: int
    line_end: int
    parent: str | None = None  # 부모 클래스/메서드명
    modifiers: list[str] | None = None
    return_type: str | None = None  # 메서드의 경우
    parameters: list[dict] | None = None  # 메서드의 경우
    
    def __post_init__(self):
        if self.modifiers is None:
            self.modifiers = []
        if self.parameters is None:
            self.parameters = []

@dataclass 
class ElementDependency:
    """요소별 의존성 정보"""
    element: CodeElement
    dependencies: dict[str, list[str]]  # 의존성 타입별 리스트
    referenced_elements: list[str]  # 참조하는 다른 요소들
    location_info: dict[str, list[dict]]  # 각 의존성이 사용된 위치 정보

class ElementLevelDependencyAnalyzer:
    """요소 단위 의존성 분석기"""
    
    def __init__(self, project_root: str, use_cache: bool = True):
        self.project_root = Path(project_root)
        self.class_to_file: dict[str, Path] = {}
        self.package_to_files: dict[str, list[Path]] = defaultdict(list)
        self.element_dependencies: dict[str, ElementDependency] = {}  # element_id -> ElementDependency
        self.use_cache = use_cache
        self.cache_file = self.project_root / ".element_deps_cache.json"
        
        # Tree-sitter 설정
        self.java_language = Language(tree_sitter_java.language(), "java")
        self.parser = Parser()
        self.parser.set_language(self.java_language)
        
        # Java 기본 타입 및 내장 클래스 정의
        self.java_primitives = {
            'int', 'boolean', 'float', 'double', 'long', 'short', 'byte', 'char', 'void'
        }
        
        self.java_builtins = {
            'String', 'Integer', 'Long', 'Double', 'Float', 'Boolean', 'Character',
            'Object', 'Class', 'System', 'Math', 'list', 'Map', 'Set', 'Collection',
            'ArrayList', 'HashMap', 'HashSet', 'LinkedList', 'TreeMap', 'TreeSet',
            'Exception', 'RuntimeException', 'Thread', 'Runnable', 'Throwable',
            'Error', 'Optional', 'Stream', 'Collectors', 'Arrays', 'Collections',
            'BigDecimal', 'BigInteger', 'Date', 'Calendar', 'UUID', 'Pattern',
            'Matcher', 'StringBuilder', 'StringBuffer', 'Number', 'Enum',
            'Comparable', 'Serializable', 'Cloneable', 'Iterable', 'Iterator'
        }
        
        self._load_cache_or_scan()
    
    def _get_node_text(self, node, source_code: bytes) -> str:
        """노드의 텍스트 내용을 반환"""
        return source_code[node.start_byte:node.end_byte].decode('utf-8')
    
    def _get_line_number(self, node) -> tuple[int, int]:
        """노드의 시작/끝 라인 번호 반환"""
        return node.start_point[0] + 1, node.end_point[0] + 1
    
    def _load_cache_or_scan(self):
        """캐시를 로드하거나 프로젝트를 새로 스캔"""
        if self.use_cache and self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                    # Path 객체로 복원
                    self.class_to_file = {k: Path(v) for k, v in cache_data.get('class_to_file', {}).items()}
                    self.package_to_files = {
                        k: [Path(p) for p in v] 
                        for k, v in cache_data.get('package_to_files', {}).items()
                    }
                print(f"캐시에서 {len(self.class_to_file)}개 클래스 정보 로드")
                return
            except Exception as e:
                print(f"캐시 로드 실패: {e}, 새로 스캔합니다.")
        
        self._scan_project()
        self._save_cache()
    
    def _save_cache(self):
        """클래스 매핑 정보를 캐시에 저장"""
        if not self.use_cache:
            return
            
        try:
            cache_data = {
                'class_to_file': {k: str(v) for k, v in self.class_to_file.items()},
                'package_to_files': {
                    k: [str(p) for p in v] 
                    for k, v in self.package_to_files.items()
                }
            }
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"캐시 저장 실패: {e}")
    
    def _scan_project(self):
        """프로젝트 전체를 스캔하여 클래스-파일 매핑을 생성"""
        java_files = list(self.project_root.rglob("*.java"))
        print(f"스캔 중: {len(java_files)}개 Java 파일")
        
        for file_path in java_files:
            try:
                package_name, class_info = self._extract_package_and_classes(file_path)
                
                # 패키지별 파일 매핑
                if package_name:
                    self.package_to_files[package_name].append(file_path)
                
                # 클래스별 파일 매핑
                for class_name, is_nested in class_info:
                    full_class_name = f"{package_name}.{class_name}" if package_name else class_name
                    self.class_to_file[full_class_name] = file_path
                    self.class_to_file[class_name] = file_path
                    
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    
    def _extract_package_and_classes(self, file_path: Path) -> tuple[str, list[tuple[str, bool]]]:
        """패키지명과 클래스명 추출"""
        with open(file_path, 'rb') as f:
            source_code = f.read()
        
        tree = self.parser.parse(source_code)
        root_node = tree.root_node
        
        package_name = ""
        class_info = []
        
        def extract_classes_from_node(node, parent_class="", depth=0):
            if node.type in ['class_declaration', 'interface_declaration', 'enum_declaration', 'record_declaration']:
                for child in node.children:
                    if child.type == 'identifier':
                        class_name = self._get_node_text(child, source_code)
                        full_name = f"{parent_class}.{class_name}" if parent_class else class_name
                        is_nested = depth > 0
                        class_info.append((full_name, is_nested))
                        
                        for nested_child in node.children:
                            if nested_child.type == 'class_body':
                                extract_classes_from_node(nested_child, full_name, depth + 1)
                        break
            else:
                for child in node.children:
                    extract_classes_from_node(child, parent_class, depth)
        
        def traverse_node(node):
            nonlocal package_name
            
            if node.type == 'package_declaration':
                for child in node.children:
                    if child.type in ['scoped_identifier', 'identifier']:
                        package_name = self._get_node_text(child, source_code)
                        break
            
            for child in node.children:
                traverse_node(child)
        
        traverse_node(root_node)
        extract_classes_from_node(root_node)
        
        return package_name, class_info
    
    def extract_element_level_dependencies(self, file_path: Path) -> dict[str, ElementDependency]:
        """파일에서 요소별 의존성을 추출"""
        with open(file_path, 'rb') as f:
            source_code = f.read()
        
        tree = self.parser.parse(source_code)
        root_node = tree.root_node
        
        # 파일의 모든 요소들을 먼저 추출
        elements = self._extract_all_elements(root_node, source_code, file_path)
        
        # 각 요소별로 의존성 분석
        element_dependencies = {}
        
        for element_id, element in elements.items():
            dependencies = self._analyze_element_dependencies(element, root_node, source_code, elements)
            element_dependencies[element_id] = ElementDependency(
                element=element,
                dependencies=dependencies['dependencies'],
                referenced_elements=dependencies['referenced_elements'],
                location_info=dependencies['location_info']
            )
        
        return element_dependencies
    
    def _extract_all_elements(self, root_node, source_code: bytes, file_path: Path) -> dict[str, CodeElement]:
        """파일의 모든 코드 요소들을 추출"""
        elements = {}
        
        def extract_elements_from_node(node, parent_name="", class_context=""):
            if node.type == 'class_declaration':
                class_element = self._extract_class_element(node, source_code, parent_name)
                if class_element:
                    element_id = f"{file_path}::{class_element.name}"
                    elements[element_id] = class_element
                    
                    # 클래스 내부 요소들 추출
                    for child in node.children:
                        if child.type == 'class_body':
                            extract_elements_from_node(child, class_element.name, class_element.name)
            
            elif node.type == 'interface_declaration':
                interface_element = self._extract_interface_element(node, source_code, parent_name)
                if interface_element:
                    element_id = f"{file_path}::{interface_element.name}"
                    elements[element_id] = interface_element
                    
                    for child in node.children:
                        if child.type == 'interface_body':
                            extract_elements_from_node(child, interface_element.name, interface_element.name)
            
            elif node.type == 'enum_declaration':
                enum_element = self._extract_enum_element(node, source_code, parent_name)
                if enum_element:
                    element_id = f"{file_path}::{enum_element.name}"
                    elements[element_id] = enum_element
                    
                    for child in node.children:
                        if child.type == 'enum_body':
                            extract_elements_from_node(child, enum_element.name, enum_element.name)
            
            elif node.type == 'method_declaration':
                method_element = self._extract_method_element(node, source_code, class_context)
                if method_element:
                    element_id = f"{file_path}::{class_context}::{method_element.name}"
                    elements[element_id] = method_element
            
            elif node.type == 'constructor_declaration':
                constructor_element = self._extract_constructor_element(node, source_code, class_context)
                if constructor_element:
                    element_id = f"{file_path}::{class_context}::{constructor_element.name}"
                    elements[element_id] = constructor_element
            
            elif node.type == 'field_declaration':
                field_elements = self._extract_field_elements(node, source_code, class_context)
                for field_element in field_elements:
                    element_id = f"{file_path}::{class_context}::{field_element.name}"
                    elements[element_id] = field_element
            
            else:
                # 다른 노드들에서도 재귀적으로 요소 찾기
                for child in node.children:
                    extract_elements_from_node(child, parent_name, class_context)
        
        extract_elements_from_node(root_node)
        return elements
    
    def _extract_class_element(self, node, source_code: bytes, parent_name: str) -> CodeElement | None:
        """클래스 요소 추출"""
        class_name = ""
        modifiers = []
        line_start, line_end = self._get_line_number(node)
        
        for child in node.children:
            if child.type == 'identifier':
                class_name = self._get_node_text(child, source_code)
            elif child.type == 'modifiers':
                modifiers = self._extract_modifiers(child, source_code)
        
        if class_name:
            return CodeElement(
                name=class_name,
                type='class',
                line_start=line_start,
                line_end=line_end,
                parent=parent_name if parent_name else None,
                modifiers=modifiers
            )
        return None
    
    def _extract_interface_element(self, node, source_code: bytes, parent_name: str) -> CodeElement | None:
        """인터페이스 요소 추출"""
        interface_name = ""
        modifiers = []
        line_start, line_end = self._get_line_number(node)
        
        for child in node.children:
            if child.type == 'identifier':
                interface_name = self._get_node_text(child, source_code)
            elif child.type == 'modifiers':
                modifiers = self._extract_modifiers(child, source_code)
        
        if interface_name:
            return CodeElement(
                name=interface_name,
                type='interface',
                line_start=line_start,
                line_end=line_end,
                parent=parent_name if parent_name else None,
                modifiers=modifiers
            )
        return None
    
    def _extract_enum_element(self, node, source_code: bytes, parent_name: str) -> CodeElement | None:
        """열거형 요소 추출"""
        enum_name = ""
        modifiers = []
        line_start, line_end = self._get_line_number(node)
        
        for child in node.children:
            if child.type == 'identifier':
                enum_name = self._get_node_text(child, source_code)
            elif child.type == 'modifiers':
                modifiers = self._extract_modifiers(child, source_code)
        
        if enum_name:
            return CodeElement(
                name=enum_name,
                type='enum',
                line_start=line_start,
                line_end=line_end,
                parent=parent_name if parent_name else None,
                modifiers=modifiers
            )
        return None
    
    def _extract_method_element(self, node, source_code: bytes, class_context: str) -> CodeElement | None:
        """메서드 요소 추출"""
        method_name = ""
        modifiers = []
        return_type = ""
        parameters = []
        line_start, line_end = self._get_line_number(node)
        
        for child in node.children:
            if child.type == 'identifier':
                method_name = self._get_node_text(child, source_code)
            elif child.type == 'modifiers':
                modifiers = self._extract_modifiers(child, source_code)
            elif child.type == 'type_identifier':
                return_type = self._get_node_text(child, source_code)
            elif child.type == 'generic_type':
                return_type = self._get_node_text(child, source_code)
            elif child.type == 'formal_parameters':
                parameters = self._extract_parameters(child, source_code)
        
        if method_name:
            return CodeElement(
                name=method_name,
                type='method',
                line_start=line_start,
                line_end=line_end,
                parent=class_context,
                modifiers=modifiers,
                return_type=return_type if return_type else None,
                parameters=parameters
            )
        return None
    
    def _extract_constructor_element(self, node, source_code: bytes, class_context: str) -> CodeElement | None:
        """생성자 요소 추출"""
        constructor_name = ""
        modifiers = []
        parameters = []
        line_start, line_end = self._get_line_number(node)
        
        for child in node.children:
            if child.type == 'identifier':
                constructor_name = self._get_node_text(child, source_code)
            elif child.type == 'modifiers':
                modifiers = self._extract_modifiers(child, source_code)
            elif child.type == 'formal_parameters':
                parameters = self._extract_parameters(child, source_code)
        
        if constructor_name:
            return CodeElement(
                name=f"{constructor_name}(constructor)",
                type='constructor',
                line_start=line_start,
                line_end=line_end,
                parent=class_context,
                modifiers=modifiers,
                parameters=parameters
            )
        return None
    
    def _extract_field_elements(self, node, source_code: bytes, class_context: str) -> list[CodeElement]:
        """필드 요소들 추출 (하나의 선언에 여러 필드가 있을 수 있음)"""
        field_elements = []
        modifiers = []
        field_type = ""
        line_start, line_end = self._get_line_number(node)
        
        for child in node.children:
            if child.type == 'modifiers':
                modifiers = self._extract_modifiers(child, source_code)
            elif child.type == 'type_identifier':
                field_type = self._get_node_text(child, source_code)
            elif child.type == 'generic_type':
                field_type = self._get_node_text(child, source_code)
            elif child.type == 'variable_declarator':
                for grandchild in child.children:
                    if grandchild.type == 'identifier':
                        field_name = self._get_node_text(grandchild, source_code)
                        field_elements.append(CodeElement(
                            name=field_name,
                            type='field',
                            line_start=line_start,
                            line_end=line_end,
                            parent=class_context,
                            modifiers=modifiers,
                            return_type=field_type if field_type else None
                        ))
        
        return field_elements
    
    def _extract_modifiers(self, node, source_code: bytes) -> list[str]:
        """접근 제한자 및 기타 수정자 추출"""
        modifiers = []
        for child in node.children:
            if child.type in ['public', 'private', 'protected', 'static', 'final', 'abstract', 'synchronized', 'volatile', 'transient', 'native', 'strictfp']:
                modifiers.append(self._get_node_text(child, source_code))
        return modifiers
    
    def _extract_parameters(self, node, source_code: bytes) -> list[dict]:
        """매개변수 정보 추출"""
        parameters = []
        
        for child in node.children:
            if child.type == 'formal_parameter':
                param_info = {'type': '', 'name': '', 'modifiers': []}
                
                for grandchild in child.children:
                    if grandchild.type == 'type_identifier':
                        param_info['type'] = self._get_node_text(grandchild, source_code)
                    elif grandchild.type == 'generic_type':
                        param_info['type'] = self._get_node_text(grandchild, source_code)
                    elif grandchild.type == 'identifier':
                        param_info['name'] = self._get_node_text(grandchild, source_code)
                    elif grandchild.type == 'modifiers':
                        param_info['modifiers'] = self._extract_modifiers(grandchild, source_code)
                
                if param_info['name']:
                    parameters.append(param_info)
        
        return parameters
    
    def _analyze_element_dependencies(self, element: CodeElement, root_node, source_code: bytes, all_elements: dict[str, CodeElement]) -> dict:
        """특정 요소의 의존성 분석"""
        dependencies = {
            'imports': [],
            'class_references': [],
            'method_calls': [],
            'field_access': [],
            'inheritance': [],
            'annotations': [],
            'generics': [],
            'exceptions': [],
            'lambda_references': [],
            'local_variables': []
        }
        
        referenced_elements = []
        location_info = defaultdict(list)
        
        # 요소의 위치에 해당하는 AST 노드를 찾기
        element_node = self._find_element_node(root_node, element, source_code)
        
        if element_node:
            # 해당 요소 내부에서만 의존성 분석
            self._analyze_node_dependencies(element_node, source_code, dependencies, location_info, referenced_elements, all_elements)
        
        # 중복 제거 및 정리 - 순서 보존하면서 중복 제거
        for key in dependencies:
            unique_deps = []
            seen = set()
            for dep in dependencies[key]:
                if dep and not self._is_java_builtin_or_primitive(dep) and dep not in seen:
                    unique_deps.append(dep)
                    seen.add(dep)
            dependencies[key] = unique_deps
        
        # referenced_elements도 중복 제거
        unique_refs = []
        seen_refs = set()
        for ref in referenced_elements:
            if ref and ref not in seen_refs:
                unique_refs.append(ref)
                seen_refs.add(ref)
        
        return {
            'dependencies': dependencies,
            'referenced_elements': unique_refs,
            'location_info': dict(location_info)
        }
    
    def _find_element_node(self, root_node, element: CodeElement, source_code: bytes):
        """요소에 해당하는 AST 노드 찾기"""
        def find_node_by_position(node):
            node_start, node_end = self._get_line_number(node)
            
            # 라인 번호와 요소 타입이 일치하는지 확인
            if (node_start == element.line_start and 
                node_end >= element.line_end and
                self._node_matches_element_type(node, element)):
                
                # 이름도 확인
                if self._node_name_matches(node, element, source_code):
                    return node
            
            # 자식 노드들에서 재귀적으로 찾기
            for child in node.children:
                result = find_node_by_position(child)
                if result:
                    return result
            
            return None
        
        return find_node_by_position(root_node)
    
    def _node_matches_element_type(self, node, element: CodeElement) -> bool:
        """노드 타입이 요소 타입과 일치하는지 확인"""
        type_mapping = {
            'class': ['class_declaration'],
            'interface': ['interface_declaration'],
            'enum': ['enum_declaration'],
            'method': ['method_declaration'],
            'constructor': ['constructor_declaration'],
            'field': ['field_declaration']
        }
        
        return node.type in type_mapping.get(element.type, [])
    
    def _node_name_matches(self, node, element: CodeElement, source_code: bytes) -> bool:
        """노드 이름이 요소 이름과 일치하는지 확인"""
        for child in node.children:
            if child.type == 'identifier':
                node_name = self._get_node_text(child, source_code)
                if element.type == 'constructor':
                    return node_name in element.name
                else:
                    return node_name == element.name
        return False
    
    def _analyze_node_dependencies(self, node, source_code: bytes, dependencies: dict, location_info: dict, referenced_elements: list, all_elements: dict):
        """노드에서 의존성 분석"""
        line_start, line_end = self._get_line_number(node)
        
        if node.type == 'object_creation_expression':
            self._extract_object_creation_dependency(node, source_code, dependencies, location_info, line_start)
        
        elif node.type == 'method_invocation':
            self._extract_method_invocation_dependency(node, source_code, dependencies, location_info, line_start, referenced_elements)
        
        elif node.type == 'field_access':
            self._extract_field_access_dependency(node, source_code, dependencies, location_info, line_start, referenced_elements)
        
        elif node.type == 'type_identifier':
            type_name = self._get_node_text(node, source_code)
            if not self._is_java_builtin_or_primitive(type_name):
                # 부모 노드가 메서드 호출이나 필드 접근이 아닌 경우에만 추가
                parent_types = ['method_invocation', 'field_access']
                if not node.parent or node.parent.type not in parent_types:
                    dependencies['class_references'].append(type_name)
                    location_info['class_references'].append({
                        'name': type_name,
                        'line': line_start,
                        'context': 'type_usage'
                    })
        
        elif node.type == 'annotation':
            self._extract_annotation_dependency(node, source_code, dependencies, location_info, line_start)
        
        elif node.type == 'local_variable_declaration':
            self._extract_local_variable_dependency(node, source_code, dependencies, location_info, line_start)
        
        elif node.type == 'cast_expression':
            self._extract_cast_dependency(node, source_code, dependencies, location_info, line_start)
        
        elif node.type == 'try_statement':
            self._extract_exception_dependency(node, source_code, dependencies, location_info, line_start)
        
        # 자식 노드들을 재귀적으로 분석
        for child in node.children:
            self._analyze_node_dependencies(child, source_code, dependencies, location_info, referenced_elements, all_elements)
    
    def _extract_object_creation_dependency(self, node, source_code: bytes, dependencies: dict, location_info: dict, line: int):
        """객체 생성 의존성 추출"""
        for child in node.children:
            if child.type == 'type_identifier':
                class_name = self._get_node_text(child, source_code)
                if not self._is_java_builtin_or_primitive(class_name):
                    dependencies['class_references'].append(class_name)
                    location_info['class_references'].append({
                        'name': class_name,
                        'line': line,
                        'context': 'object_creation'
                    })
    
    def _extract_method_invocation_dependency(self, node, source_code: bytes, dependencies: dict, location_info: dict, line: int, referenced_elements: list):
        """메서드 호출 의존성 추출 (개선된 버전)"""
        
        # 노드의 전체 텍스트로 디버깅
        method_text = self._get_node_text(node, source_code).strip()
        
        # 직접적인 메서드 이름 찾기
        for child in node.children:
            if child.type == 'identifier':
                method_name = self._get_node_text(child, source_code).strip()
                # 메서드 호출 기록 (Java 키워드나 내장 메서드 제외)
                if method_name and not self._is_java_builtin_or_primitive(method_name) and not method_name in ['for', 'if', 'while', 'try', 'catch']:
                    dependencies['method_calls'].append(method_name)
                    location_info['method_calls'].append({
                        'name': method_name,
                        'line': line,
                        'context': 'direct_method_call'
                    })
                    referenced_elements.append(f"method:{method_name}")
            
            elif child.type == 'field_access':
                # Class.method() 또는 object.method() 형태
                field_text = self._get_node_text(child, source_code).strip()
                if '.' in field_text:
                    parts = field_text.split('.')
                    if len(parts) >= 2:
                        target_obj = parts[0].strip()
                        method_name = parts[1].strip()
                        
                        # 대문자로 시작하면 클래스, 소문자면 객체 참조
                        if target_obj and len(target_obj) > 0:
                            if target_obj[0].isupper():
                                # 정적 메서드 호출 (Class.method)
                                if not self._is_java_builtin_or_primitive(target_obj):
                                    dependencies['class_references'].append(target_obj)
                                    location_info['class_references'].append({
                                        'name': target_obj,
                                        'line': line,
                                        'context': 'static_method_target'
                                    })
                                referenced_elements.append(f"method:{target_obj}.{method_name}")
                            else:
                                # 인스턴스 메서드 호출 (object.method)
                                if target_obj not in ['this', 'super']:
                                    dependencies['field_access'].append(target_obj)
                                    location_info['field_access'].append({
                                        'name': target_obj,
                                        'line': line,
                                        'context': 'instance_method_target'
                                    })
                                referenced_elements.append(f"method:{target_obj}.{method_name}")
                        
                        # 메서드 이름 기록
                        if method_name and not self._is_java_builtin_or_primitive(method_name):
                            dependencies['method_calls'].append(method_name)
                            location_info['method_calls'].append({
                                'name': method_name,
                                'line': line,
                                'context': 'chained_method_call',
                                'target': target_obj
                            })
    
    def _extract_field_access_dependency(self, node, source_code: bytes, dependencies: dict, location_info: dict, line: int, referenced_elements: list):
        """필드 접근 의존성 추출"""
        field_text = self._get_node_text(node, source_code)
        
        if '.' in field_text:
            parts = field_text.split('.')
            if len(parts) >= 2:
                class_name = parts[0]
                field_name = parts[1]
                
                if class_name and class_name[0].isupper():
                    dependencies['class_references'].append(class_name)
                    location_info['class_references'].append({
                        'name': class_name,
                        'line': line,
                        'context': 'static_field_access'
                    })
                
                dependencies['field_access'].append(field_name)
                location_info['field_access'].append({
                    'name': field_name,
                    'line': line,
                    'context': 'field_access',
                    'target_class': class_name
                })
                referenced_elements.append(f"field:{class_name}.{field_name}")
    
    def _extract_annotation_dependency(self, node, source_code: bytes, dependencies: dict, location_info: dict, line: int):
        """어노테이션 의존성 추출"""
        for child in node.children:
            if child.type == 'identifier':
                annotation_name = self._get_node_text(child, source_code)
                dependencies['annotations'].append(annotation_name)
                location_info['annotations'].append({
                    'name': annotation_name,
                    'line': line,
                    'context': 'annotation'
                })
                break
    
    def _extract_local_variable_dependency(self, node, source_code: bytes, dependencies: dict, location_info: dict, line: int):
        """지역 변수 선언 의존성 추출"""
        var_type = ""
        var_name = ""
        
        for child in node.children:
            if child.type == 'type_identifier':
                var_type = self._get_node_text(child, source_code)
            elif child.type == 'generic_type':
                var_type = self._get_node_text(child, source_code)
            elif child.type == 'variable_declarator':
                for grandchild in child.children:
                    if grandchild.type == 'identifier':
                        var_name = self._get_node_text(grandchild, source_code)
                        break
        
        if var_type and not self._is_java_builtin_or_primitive(var_type):
            dependencies['local_variables'].append(f"{var_name}:{var_type}")
            dependencies['class_references'].append(var_type)
            location_info['local_variables'].append({
                'name': var_name,
                'type': var_type,
                'line': line,
                'context': 'local_variable_declaration'
            })
    
    def _extract_cast_dependency(self, node, source_code: bytes, dependencies: dict, location_info: dict, line: int):
        """캐스트 표현식 의존성 추출"""
        for child in node.children:
            if child.type == 'type_identifier':
                cast_type = self._get_node_text(child, source_code)
                if not self._is_java_builtin_or_primitive(cast_type):
                    dependencies['class_references'].append(cast_type)
                    location_info['class_references'].append({
                        'name': cast_type,
                        'line': line,
                        'context': 'cast_expression'
                    })
    
    def _extract_exception_dependency(self, node, source_code: bytes, dependencies: dict, location_info: dict, line: int):
        """예외 처리 의존성 추출"""
        for child in node.children:
            if child.type == 'catch_clause':
                for grandchild in child.children:
                    if grandchild.type == 'catch_formal_parameter':
                        for ggchild in grandchild.children:
                            if ggchild.type == 'type_identifier':
                                exception_type = self._get_node_text(ggchild, source_code)
                                if not self._is_java_builtin_or_primitive(exception_type):
                                    dependencies['exceptions'].append(exception_type)
                                    location_info['exceptions'].append({
                                        'name': exception_type,
                                        'line': line,
                                        'context': 'exception_handling'
                                    })
    
    def _is_java_builtin_or_primitive(self, class_name: str) -> bool:
        """자바 내장 클래스 또는 기본 타입인지 확인"""
        if not class_name:
            return True
        
        return (class_name in self.java_primitives or
                class_name in self.java_builtins or
                class_name.startswith('java.') or 
                class_name.startswith('javax.') or
                class_name.startswith('sun.') or
                len(class_name) == 1)  # 제네릭 타입 파라미터
    
    def analyze_file_elements(self, file_path: Path, top_n: int = 10) -> dict[str, Any]:
        """파일의 모든 요소별 의존성 분석"""
        print(f"Analyzing elements in: {file_path}")
        
        element_dependencies = self.extract_element_level_dependencies(file_path)
        
        # 통계 계산
        stats = {
            'total_elements': len(element_dependencies),
            'elements_by_type': defaultdict(int),
            'dependency_stats': defaultdict(int),
            'most_dependent_elements': [],
            'circular_references': [],
            'top_n_limit': top_n  # 설정된 제한값 기록
        }
        
        # 의존性이 많은 요소들을 효율적으로 찾기 (heapq 사용)
        import heapq
        
        # 상위 N개만 유지하는 최소 힙 사용
        top_elements = []
        element_counter = 0  # 고유 식별자로 사용
        
        for element_id, elem_dep in element_dependencies.items():
            stats['elements_by_type'][elem_dep.element.type] += 1
            
            total_deps = sum(len(deps) for deps in elem_dep.dependencies.values())
            stats['dependency_stats'][elem_dep.element.type] += total_deps
            
            element_info = {
                'element': f"{elem_dep.element.type}:{elem_dep.element.name}",
                'total_dependencies': total_deps,
                'line': f"{elem_dep.element.line_start}-{elem_dep.element.line_end}",
                'element_type': elem_dep.element.type
            }
            
            # top_n이 0 이하면 모든 요소 포함
            if top_n <= 0:
                top_elements.append((total_deps, element_counter, element_info))
            else:
                # 힙 크기가 top_n 미만이면 그냥 추가
                if len(top_elements) < top_n:
                    heapq.heappush(top_elements, (total_deps, element_counter, element_info))
                # 현재 요소가 힙의 최소값보다 크면 교체
                elif total_deps > top_elements[0][0]:
                    heapq.heapreplace(top_elements, (total_deps, element_counter, element_info))
            
            element_counter += 1
        
        # 힙에서 꺼내서 내림차순으로 정렬
        if top_n <= 0:
            # 모든 요소를 포함하는 경우 정렬
            stats['most_dependent_elements'] = [
                elem_info for _, _, elem_info in sorted(top_elements, key=lambda x: x[0], reverse=True)
            ]
        else:
            # 상위 N개만 포함
            stats['most_dependent_elements'] = [
                elem_info for _, _, elem_info in sorted(top_elements, key=lambda x: x[0], reverse=True)
            ]
        
        return {
            'file_path': str(file_path),
            'element_dependencies': {
                element_id: {
                    'element': asdict(elem_dep.element),
                    'dependencies': elem_dep.dependencies,
                    'referenced_elements': elem_dep.referenced_elements,
                    'location_info': elem_dep.location_info
                }
                for element_id, elem_dep in element_dependencies.items()
            },
            'statistics': dict(stats)
        }

    def generate_element_dependency_report(self, target_file: str, top_n: int = 10) -> dict[str, Any]:
        """요소 단위 의존성 분석 보고서 생성"""
        target_path = Path(target_file)
        if not target_path.exists():
            if target_file in self.class_to_file:
                target_path = self.class_to_file[target_file]
            else:
                raise FileNotFoundError(f"Target file not found: {target_file}")
        
        analysis_result = self.analyze_file_elements(target_path, top_n)
        
        # 추가 분석
        report = {
            'analysis_type': 'element-level-dependency',
            'target_file': str(target_path),
            'top_n_limit': top_n,
            'timestamp': json.dumps(None),  # 현재 시간으로 대체 가능
            'summary': self._generate_analysis_summary(analysis_result),
            'detailed_analysis': analysis_result,
            'recommendations': self._generate_recommendations(analysis_result),
            'dependency_matrix': self._build_dependency_matrix(analysis_result)
        }
        
        return report
    
    def _generate_analysis_summary(self, analysis_result: dict) -> dict:
        """분석 요약 생성"""
        stats = analysis_result['statistics']
        element_deps = analysis_result['element_dependencies']
        
        # 복잡도 분석
        high_complexity_elements = [
            elem for elem in stats['most_dependent_elements'] 
            if elem['total_dependencies'] > 10
        ]
        
        # 의존성 패턴 분석
        dependency_patterns = defaultdict(int)
        for elem_id, elem_data in element_deps.items():
            for dep_type, deps in elem_data['dependencies'].items():
                if deps:
                    dependency_patterns[dep_type] += len(deps)
        
        return {
            'total_elements_analyzed': stats['total_elements'],
            'elements_by_type': dict(stats['elements_by_type']),
            'high_complexity_elements_count': len(high_complexity_elements),
            'most_common_dependency_types': dict(sorted(dependency_patterns.items(), key=lambda x: x[1], reverse=True)[:5]),
            'average_dependencies_per_element': sum(dependency_patterns.values()) / max(stats['total_elements'], 1),
            'complexity_indicators': {
                'methods_with_high_dependencies': len([e for e in high_complexity_elements if 'method:' in e['element']]),
                'classes_with_high_dependencies': len([e for e in high_complexity_elements if 'class:' in e['element']]),
                'fields_with_dependencies': sum(1 for elem_data in element_deps.values() if elem_data['element']['type'] == 'field' and any(elem_data['dependencies'].values()))
            }
        }
    
    def _generate_recommendations(self, analysis_result: dict) -> list[str]:
        """개선 권장사항 생성"""
        recommendations = []
        stats = analysis_result['statistics']
        
        # 복잡도 기반 권장사항
        high_complexity = [e for e in stats['most_dependent_elements'] if e['total_dependencies'] > 15]
        if high_complexity:
            recommendations.append(f"High complexity detected: {len(high_complexity)} elements have >15 dependencies. Consider refactoring.")
        
        # 메서드 복잡도
        method_complexity = [e for e in stats['most_dependent_elements'] if 'method:' in e['element'] and e['total_dependencies'] > 10]
        if method_complexity:
            recommendations.append(f"{len(method_complexity)} methods have high dependency count. Consider breaking them into smaller methods.")
        
        # 클래스 복잡도
        class_complexity = [e for e in stats['most_dependent_elements'] if 'class:' in e['element'] and e['total_dependencies'] > 20]
        if class_complexity:
            recommendations.append(f"{len(class_complexity)} classes have very high dependency count. Consider applying Single Responsibility Principle.")
        
        # 의존성 패턴 기반 권장사항
        element_deps = analysis_result['element_dependencies']
        annotation_heavy = sum(1 for elem_data in element_deps.values() if len(elem_data['dependencies'].get('annotations', [])) > 5)
        if annotation_heavy > 0:
            recommendations.append(f"{annotation_heavy} elements are annotation-heavy. Review if all annotations are necessary.")
        
        return recommendations
    
    def _build_dependency_matrix(self, analysis_result: dict) -> dict:
        """의존성 매트릭스 구성"""
        matrix = {}
        element_deps = analysis_result['element_dependencies']
        
        for elem_id, elem_data in element_deps.items():
            element_name = f"{elem_data['element']['type']}:{elem_data['element']['name']}"
            matrix[element_name] = {}
            
            for dep_type, deps in elem_data['dependencies'].items():
                if deps:
                    matrix[element_name][dep_type] = {
                        'count': len(deps),
                        'dependencies': deps[:10] if len(deps) > 10 else deps,  # 처음 10개만 표시
                        'truncated': len(deps) > 10
                    }
        
        return matrix
    
    def find_element_usage(self, target_element: str, search_in_file: str = None) -> dict:
        """특정 요소가 어디서 사용되는지 찾기"""
        usage_results = {
            'target_element': target_element,
            'usages': []
        }
        
        print(f"Searching for '{target_element}' usage...")
        
        search_files = [Path(search_in_file)] if search_in_file else list(self.project_root.rglob("*.java"))
        
        for file_path in search_files:
            try:
                print(f"  Analyzing file: {file_path}")
                element_deps = self.extract_element_level_dependencies(file_path)
                
                for elem_id, elem_dep in element_deps.items():
                    # 디버깅: 각 요소가 어떤 의존성을 가지는지 출력
                    element_info = f"{elem_dep.element.type}:{elem_dep.element.name}"
                    
                    # 1. 메서드 이름으로 직접 검색
                    for dep_type, deps in elem_dep.dependencies.items():
                        if target_element in deps:
                            usage_results['usages'].append({
                                'file': str(file_path),
                                'using_element': element_info,
                                'line_range': f"{elem_dep.element.line_start}-{elem_dep.element.line_end}",
                                'dependency_type': dep_type,
                                'usage_context': f'found_in_{dep_type}'
                            })
                            print(f"    Found in {dep_type}: {element_info}")
                    
                    # 2. referenced_elements에서 찾기
                    target_variations = [
                        target_element,
                        f"method:{target_element}",
                        f"field:{target_element}",
                        f"class:{target_element}"
                    ]
                    
                    for variation in target_variations:
                        if variation in elem_dep.referenced_elements:
                            usage_results['usages'].append({
                                'file': str(file_path),
                                'using_element': element_info,
                                'line_range': f"{elem_dep.element.line_start}-{elem_dep.element.line_end}",
                                'usage_context': 'referenced_element',
                                'target_variation': variation
                            })
                            print(f"    Found as reference: {variation} in {element_info}")
                    
                    # 3. 요소 자체가 찾는 대상인지 확인 (메서드 정의 등)
                    if elem_dep.element.name == target_element:
                        usage_results['usages'].append({
                            'file': str(file_path),
                            'using_element': element_info,
                            'line_range': f"{elem_dep.element.line_start}-{elem_dep.element.line_end}",
                            'usage_context': 'element_definition',
                            'element_type': elem_dep.element.type
                        })
                        print(f"    Found definition: {element_info}")
            
            except Exception as e:
                print(f"Error analyzing {file_path}: {e}")
        
        # 중복 제거
        seen = set()
        unique_usages = []
        for usage in usage_results['usages']:
            usage_key = (usage['file'], usage['using_element'], usage.get('line_range'))
            if usage_key not in seen:
                unique_usages.append(usage)
                seen.add(usage_key)
        
        usage_results['usages'] = unique_usages
        print(f"Total unique usages found: {len(unique_usages)}")
        
        return usage_results


def main():
    """CLI 인터페이스"""
    parser = argparse.ArgumentParser(description='Element-Level Java Dependency Analyzer')
    parser.add_argument('project_root', help='Java 프로젝트 루트 디렉토리')
    parser.add_argument('target_file', help='분석할 대상 파일')
    
    parser.add_argument('--report-file', '-r', help='분석 보고서를 저장할 JSON 파일')
    parser.add_argument('--no-cache', action='store_true', help='캐시 사용 안함')
    parser.add_argument('--find-usage', help='특정 요소의 사용처 찾기 (예: "MyClass" 또는 "methodName")')
    parser.add_argument('--top-n', type=int, default=10, 
                       help='표시할 최대 복잡한 요소 개수 (0=모든 요소 표시)')
    parser.add_argument('--element-type', choices=['class', 'method', 'field', 'constructor', 'all'], 
                       default='all', help='분석할 요소 타입 필터')
    parser.add_argument('--min-dependencies', type=int, default=0, 
                       help='최소 의존성 개수 (이 수치 이상의 의존성을 가진 요소만 표시)')
    parser.add_argument('--verbose', '-v', action='store_true', help='상세 출력')
    
    args = parser.parse_args()
    
    try:
        # 분석기 초기화
        print(f"Initializing element-level analyzer for project: {args.project_root}")
        analyzer = ElementLevelDependencyAnalyzer(
            project_root=args.project_root,
            use_cache=not args.no_cache
        )
        
        if args.find_usage:
            # 특정 요소 사용처 찾기
            print(f"\nFinding usage of element: {args.find_usage}")
            usage_results = analyzer.find_element_usage(args.find_usage, args.target_file)
            
            print(f"Found {len(usage_results['usages'])} usages:")
            for usage in usage_results['usages']:
                print(f"  - {usage['using_element']} in {usage['file']} (lines {usage['line_range']})")
                if args.verbose and 'dependency_type' in usage:
                    print(f"    Type: {usage['dependency_type']}")
        
        else:
            # 기본 요소별 의존성 분석
            print(f"\nAnalyzing element-level dependencies for: {args.target_file}")
            report = analyzer.generate_element_dependency_report(args.target_file, args.top_n)
            
            # 결과 출력
            summary = report['summary']
            print(f"\n=== Element Analysis Summary ===")
            print(f"Total elements analyzed: {summary['total_elements_analyzed']}")
            print(f"Elements by type: {summary['elements_by_type']}")
            print(f"High complexity elements: {summary['high_complexity_elements_count']}")
            print(f"Average dependencies per element: {summary['average_dependencies_per_element']:.2f}")
            
            if args.top_n > 0:
                print(f"Showing top {args.top_n} most complex elements")
            else:
                print("Showing all elements (no limit)")
            
            # 상세 정보 출력
            if args.verbose:
                print(f"\n=== Detailed Element Dependencies ===")
                element_deps = report['detailed_analysis']['element_dependencies']
                
                for elem_id, elem_data in element_deps.items():
                    element = elem_data['element']
                    dependencies = elem_data['dependencies']
                    
                    # 요소 타입 필터링
                    if args.element_type != 'all' and element['type'] != args.element_type:
                        continue
                    
                    # 최소 의존성 개수 필터링
                    total_deps = sum(len(deps) for deps in dependencies.values())
                    if total_deps < args.min_dependencies:
                        continue
                    
                    print(f"\n{element['type'].upper()}: {element['name']}")
                    print(f"  Location: Lines {element['line_start']}-{element['line_end']}")
                    if element['modifiers']:
                        print(f"  Modifiers: {', '.join(element['modifiers'])}")
                    if element['return_type']:
                        print(f"  Type/Return: {element['return_type']}")
                    
                    print(f"  Dependencies ({total_deps} total):")
                    for dep_type, deps in dependencies.items():
                        if deps:
                            print(f"    {dep_type}: {deps}")
                    
                    if elem_data['referenced_elements']:
                        print(f"  Referenced elements: {elem_data['referenced_elements']}")
            
            # 권장사항 출력
            if report['recommendations']:
                print(f"\n=== Recommendations ===")
                for i, rec in enumerate(report['recommendations'], 1):
                    print(f"{i}. {rec}")
            
            # 보고서 저장
            if args.report_file:
                with open(args.report_file, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
                print(f"\nDetailed report saved to: {args.report_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    main()

 
# 1. 기본 요소별 의존성 분석:
# poetry run python analyzer.py ../samples/map_example ../samples/map_example/com/example/service/ExampleService.java --verbose
# poetry run python analyzer.py ../samples/map_example2 ../samples/map_example2/com/example/service/ExampleService.java --verbose
#
# 2. 특정 요소의 사용처 찾기:
# poetry run python analyzer.py ../samples/map_example ../samples/map_example/com/example/service/ExampleService.java --find-usage "processData"
# poetry run python analyzer.py ../samples/map_example2 ../samples/map_example2/com/example/service/ExampleService.java --find-usage "processData"
# poetry run python analyzer.py ../samples/map_example2 ../samples/map_example2/com/example/service/ExampleService.java --find-usage "Person"
# poetry run python analyzer.py ../samples/map_example2 ../samples/map_example2/com/example/service/ExampleService.java --find-usage "getPerson"
#
# 3. 메서드만 분석 (10개 이상 의존성):
# poetry run python analyzer.py ../samples/map_example target.java --element-type method --min-dependencies 10
#
# 4. 상세 보고서 저장:
# poetry run python analyzer.py ../samples/map_example target.java --report-file element_analysis.json --verbose
