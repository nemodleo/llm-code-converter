import argparse
import re
from difflib import unified_diff
from difflib import SequenceMatcher
from typing import Optional, Union, List, Dict, Any, Tuple

from pydantic import BaseModel, Field, model_validator

from aiconvertor.agent import Agent
from aiconvertor.java_utils_tree_sitter import split_java_code
from aiconvertor.java_utils_tree_sitter import matches_regardless_of_spacing
from aiconvertor.java_utils_tree_sitter import get_ast
from aiconvertor.prompt_handler import PromptHandler
from aiconvertor.prompt_handler import load_contexts
from aiconvertor.rag.retriever import ApiRetriever
from aiconvertor.incontext.retriever import CaseRetriever
from snucse_2501_aiconvertor.aiconvertor.dependency.vo_generator import VOGenerator


class ConversionConfig(BaseModel):
    """변환 설정을 위한 Pydantic 모델"""
    model: str = Field(default='qwen2.5-coder:7b', description='사용할 모델')
    mode: str = Field(default='module', description='변환 모드: module, page, line')
    use_diff: bool = Field(default=False, description='diff 정보 포함 여부')
    use_reflextion: bool = Field(default=False, description='피드백 기반 반복 개선 사용 여부')
    use_prompt_normalization: bool = Field(default=False, description='프롬프트 정규화 사용 여부')
    use_prefix_output: bool = Field(default=True, description='```java 코드 블록 사용 여부')
    use_vo_generator: bool = Field(default=False, description='VO 생성기 사용 여부')
    vo_package: Optional[str] = Field(default=None, description='VO 패키지')
    vo_class_name: Optional[str] = Field(default=None, description='VO 클래스 이름')
    project_root: Optional[str] = Field(default=None, description='프로젝트 루트 경로')
    vo_file: Optional[str] = Field(default=None, description='VO 파일 경로')
    use_api_rag: bool = Field(default=False, description='Proworks5 api RAG 사용 여부')
    use_case_rag: bool = Field(default=False, description='Case RAG 사용 여부')
    max_line_limit_offset: Optional[int] = Field(default=None, description='Agent 응답 라인 수 제한 오프셋')
    skip_non_map: bool = Field(default=False, description='Map 관련 코드가 없는 경우 변환 건너뛰기')
    context: Optional[str] = Field(default=None, description='컨텍스트 파일 경로')
    java: str = Field(default="data/samples/file_sample_original/SampleTaskServiceImpl_in.java", description='입력 Java 파일 경로')
    gt: str = Field(default="data/samples/file_sample_original/SampleTaskServiceImpl_out.java", description='Ground truth Java 파일 경로')
    iterations: int = Field(default=1, description='최대 반복 횟수')
    verbose: bool = Field(default=False, description='상세 출력 모드')

    @model_validator(mode='after')
    def validate_vo_options(self):
        """VO 관련 옵션 유효성 검사"""
        if self.use_vo_generator and self.vo_file:
            raise ValueError("use_vo_generator 와 vo_file 은 동시에 사용할 수 없습니다.")
        return self

    class Config:
        """Pydantic 설정"""
        validate_assignment = True
        extra = 'forbid'  # 정의되지 않은 필드 금지


COLOR_MAP = {
    "reset": "\033[0m",
    "cyan": "\033[96m",
    "green": "\033[92m",
    "magenta": "\033[95m",
    "yellow": "\033[93m",
}

def print_color(body, color):
    color_code = COLOR_MAP.get(color, COLOR_MAP["reset"])
    print(color_code + body + COLOR_MAP["reset"])


class AIConverter:
    """AI로 Code를 변환하는 클래스"""
    def __init__(self,
                 agent: Agent,
                 use_diff: bool = False,
                 use_reflextion: bool = False,
                 use_prompt_normalization: bool = False,
                 use_prefix_output: bool = False,
                 use_vo_generator: bool = False,
                 vo_file: str = None,
                 use_api_rag: bool = False,
                 use_case_rag: bool = False,
                 iterations: int = 1,
                 skip_non_map: bool = False,
                 max_line_limit_offset: int = None,
                 project_root: str = None,
                 vo_package: str = None,
                 vo_class_name: str = None):
        self.agent = agent
        self.prompt_handler = PromptHandler()
        self.use_diff = use_diff
        self.use_reflextion = use_reflextion
        self.use_vo_generator = use_vo_generator
        self.vo_file = vo_file
        self.use_api_rag = use_api_rag
        self.use_case_rag = use_case_rag
        self.use_prompt_normalization = use_prompt_normalization
        self.use_prefix_output = use_prefix_output
        self.iterations = iterations
        self.skip_non_map = skip_non_map
        self.max_line_limit_offset = max_line_limit_offset

        self.vo_code: str | None = None
        if use_vo_generator:
            vo_generator = VOGenerator(
                project_root=project_root,
                vo_package=vo_package,
                vo_class_name=vo_class_name
            )
            self.vo_code = vo_generator.generate_vo_class()
        elif vo_file:
            self.vo_code = load_contexts(vo_file)
        else:
            pass


        self.api_retriever = None
        if use_api_rag:
            _embedding_model_name = "microsoft/codebert-base"
            self.api_retriever = ApiRetriever(
                vectorstore_path=f"data/db/proworks5_vectorstore_{_embedding_model_name.split('/')[-1]}",
                embedding_model_name=_embedding_model_name
            )

        self.case_retriever = None
        if use_case_rag:
            self.case_retriever = CaseRetriever()
            self.case_retriever.load_embedding_data()

    
    def load_java_files(self, 
                       input_java_path: str,
                       context_path: str = None,
                       gt_java_path: str = None) -> dict[str, any]:
        """Java 파일들과 컨텍스트 로드"""
        
        # 컨텍스트 로드
        if context_path:
            contexts = load_contexts(context_path)
        else:
            contexts = ""
        # TODO build contexts
        
        # Java 코드 로드
        java_code = load_contexts(input_java_path)
        
        # Ground truth 코드 로드 (선택적)
        gt_java_code = None
        if gt_java_path:
            gt_java_code = load_contexts(gt_java_path)
        else:
            gt_java_code = java_code  # fallback
        
        return {
            'contexts': contexts,
            'java_code': java_code,
            'gt_java_code': gt_java_code,
        }
    
    def print_extracted_methods(self, data: dict[str, any]):
        """추출된 메서드들 출력"""
        
        fn_names = data['function_names']
        gt_fn_bodies = data['gt_function_bodies']
        
        for fn in fn_names:
            print(f"\nFunction: {fn}")
            print(gt_fn_bodies.get(fn, "[Not Found in GT]"))

    
    # 코드 파싱: 앞쪽 주석, 들여쓰기, 실제 코드, 뒤쪽 주석 분리
    def parse_code_structure(self, code_text):
        lines = code_text.split('\n')
        
        # 앞쪽 주석과 공백 라인 찾기
        prefix_lines = []
        start_idx = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped == '' or stripped.startswith('//') or stripped.startswith('/*') or stripped.endswith('*/'):
                prefix_lines.append(line)
                start_idx = i + 1
            else:
                break
        
        # 뒤쪽 주석과 공백 라인 찾기
        postfix_lines = ['```java']
        end_idx = len(lines)
        for i in range(len(lines) - 1, -1, -1):
            stripped = lines[i].strip()
            if stripped == '' or stripped.startswith('//') or stripped.startswith('/*') or stripped.endswith('*/'):
                postfix_lines.insert(0, lines[i])
                end_idx = i
            else:
                break
        
        # 실제 코드 부분
        code_lines = lines[start_idx:end_idx]
        
        # 들여쓰기 추출 (첫 번째 비어있지 않은 코드 라인에서)
        indent_prefix = ""
        for line in code_lines:
            if line.strip():
                for char in line:
                    if char in [' ', '\t']:
                        indent_prefix += char
                    else:
                        break
                break
        
        # 정규화된 코드 (들여쓰기 제거)
        normalized_lines = []
        for line in code_lines:
            if line.strip():
                # 공통 들여쓰기 제거
                if line.startswith(indent_prefix):
                    normalized_lines.append(line[len(indent_prefix):])
                else:
                    normalized_lines.append(line.lstrip())
            else:
                normalized_lines.append('')
        
        normalize_code = '\n'.join(normalized_lines).strip()
        prefix_output = '\n'.join(prefix_lines)
        postfix_output = '\n'.join(postfix_lines)
        
        return normalize_code, indent_prefix, prefix_output, postfix_output

    def recover_original_code(self, normalize_code, indent_prefix, prefix_output, postfix_output):
        # 정규화된 코드에 들여쓰기 다시 적용
        indented_lines = []
        for line in normalize_code.split('\n'):
            if line.strip():
                indented_lines.append(indent_prefix + line)
            else:
                indented_lines.append('')
        
        # 전체 조합
        parts = []
        if prefix_output:
            parts.append(prefix_output)
        if indented_lines:
            parts.append('\n'.join(indented_lines))
        if postfix_output:
            parts.append(postfix_output)
        
        return '\n'.join(parts)

    def _build_contexts(self, contexts: str, code: str) -> str:
        """컨텍스트 빌드"""
        if self.vo_code:
            vo_code_prompt = f"<vo_class>\n{self.vo_code}\n</vo_class>\n\n"
            contexts += vo_code_prompt

        if self.use_api_rag:
            api_prompt = self.api_retriever.get_prompt(code)
            if api_prompt is not None:
                contexts += api_prompt

        if self.use_case_rag:
            case_prompt = self.case_retriever.get_prompt(code)
            if case_prompt is not None:
                contexts += case_prompt

        return contexts

    def _generate_diff(self, original_code: str, candidate_code: str) -> str:
        """diff 생성 (공통 함수)"""
        return '\n'.join(unified_diff(
            original_code.splitlines(),
            candidate_code.splitlines(),
            fromfile='input',
            tofile='candidate',
            lineterm=''
        ))

    def _call_agent_and_extract_code(self, prompt: str, stage: str, max_lines: int) -> str:
        """agent 호출 및 코드 추출 (공통 함수)"""
        response = self.agent(prompt, clear_messages=True, max_lines=max_lines)
        extracted_code = self.prompt_handler.extract_code_from_response(response, self.use_prefix_output)
        self._print_prompt_response(prompt, response, stage, extracted_code)
        return extracted_code

    def _generate_feedback(self, contexts: str, code: str, prev_output: str, max_lines: int) -> str:
        """피드백 생성 전용 함수"""
        diff_text = None
        
        # diff 생성 (필요한 경우)
        if self.use_diff:
            diff_text = self._generate_diff(code, prev_output)
        
        # 피드백 생성 프롬프트 빌드
        prompt = self.prompt_handler.build_feedback_prompt(
            contexts, prev_output, diff_text, self.use_diff
        )
        
        # agent 호출 및 피드백 추출
        response = self.agent(prompt, clear_messages=True, max_lines=max_lines)
        feedback = self.prompt_handler.extract_feedback_from_response(response)
        self._print_prompt_response(prompt, response, "Feedback Generation", None)
        
        return feedback

    def _generate_diff_if_needed(self, code: str, prev_output: str) -> str | None:
        """diff 생성 (필요한 경우에만)"""
        return self._generate_diff(code, prev_output) if self.use_diff else None

    def _perform_code_correction(self, contexts: str, code: str, prev_output: str, 
                                feedback: str | None, stage: str, max_lines: int) -> str:
        """코드 수정 공통 함수 (피드백 있/없 모두 처리)"""
        
        # diff 생성 (필요한 경우)
        diff_text = self._generate_diff_if_needed(code, prev_output)
        
        # 수정 프롬프트 빌드
        prompt = self.prompt_handler.build_correction_prompt(
            contexts, prev_output, code,
            feedback, diff_text, self.use_diff
        )
        
        return self._call_agent_and_extract_code(prompt, stage, max_lines)

    def _perform_initial_conversion(self, contexts: str, normalize_code: str, prefix_output: str, max_lines: int) -> str:
        """첫 번째 시도: 초기 변환"""
        prompt = self.prompt_handler.build_initial_prompt(
            contexts, normalize_code, prefix_output
        )
        
        return self._call_agent_and_extract_code(prompt, "Initial Conversion", max_lines)

    def _perform_reflexion_conversion(self, contexts: str, code: str, prev_output: str, max_lines: int) -> str:
        """두 번째 시도: 피드백 생성 및 기반 수정 (reflexion 모드)"""
        
        # 피드백 생성
        feedback = self._generate_feedback(contexts, code, prev_output, max_lines)

        # 피드백 기반 수정
        return self._perform_code_correction(
            contexts, code, prev_output, feedback, 
            "Feedback-based Correction", max_lines
        )

    def _perform_iterative_improvement(self, contexts: str, code: str, prev_output: str, max_lines: int) -> str:
        """반복 개선: diff 정보 기반 수정"""
        
        # 피드백 없이 수정
        return self._perform_code_correction(
            contexts, code, prev_output, None, 
            "Iterative Improvement", max_lines
        )

    def convert_code(self,
                     contexts: str,
                     code: str,
                     gt_code: str) -> dict[str, any]:
        """단일 변환"""    
        
        # Map 관련 코드가 없으면 원본 코드 그대로 리턴 (옵션이 활성화된 경우)
        if self.skip_non_map:
            if not re.search(r"\bmap\.(get|put|remove)\b|Map", code):
                print("ℹ️  No map operations found. Returning original code.")
                return {
                    'original_code': code,
                    'converted_code': code,
                    'is_correct': True,  # 변환이 필요없으므로 정답으로 처리
                    'iterations': 0,
                    'ground_truth': gt_code,
                    'skipped': True
                }
        
        if self.use_prompt_normalization:
            normalize_code, indent_prefix, prefix_output, postfix_output = self.parse_code_structure(code)
            prefix_output = "\n" +  postfix_output if self.use_prefix_output else "\n"
        else:
            normalize_code = code
            indent_prefix = ""
            prefix_output = "\n" + "```java\n" if self.use_prefix_output else "\n"
            postfix_output = ""

        diff_text = None
        prev_output = None
        
        # 라인 수 제한 계산
        max_lines = None
        if self.max_line_limit_offset is not None:
            code_lines = len(normalize_code.splitlines())
            max_lines = code_lines + self.max_line_limit_offset
        
        for i in range(self.iterations):
            print(f"\n--- Iteration {i + 1} ---")
            
            if prev_output is None:
                prev_output = self._perform_initial_conversion(contexts, normalize_code, prefix_output, max_lines)
            elif self.use_reflextion:
                prev_output = self._perform_reflexion_conversion(contexts, code, prev_output, max_lines)
            else:
                prev_output = self._perform_iterative_improvement(contexts, code, prev_output, max_lines)

            # 프롬프트 정규화 사용 시 원본 코드로 복구
            if self.use_prompt_normalization:
                prev_output = self.recover_original_code(prev_output, indent_prefix, prefix_output, postfix_output)

            # 결과 평가
            is_correct = self._evaluate_output(prev_output, gt_code)['exact_match']
            if is_correct:
                break
        
        # 최종 결과
        print("\n" + "="*50)
        print("Final corrected method:")
        print(prev_output)
        
        # 최종 평가
        is_correct = self._evaluate_output(prev_output, gt_code)['exact_match']
        
        return {
            'original_code': code,
            'converted_code': prev_output,
            'is_correct': is_correct,
            'iterations': i + 1,
            'ground_truth': gt_code
        }
    
    def convert_all_modules(self, data: dict[str, any], skip_non_map_code: bool = False) -> list[dict[str, any]]:
        """모든 모듈 변환 (Module 단위)"""
        
        results = []
        contexts = data['contexts']
        java_code = data['java_code']
        gt_java_code = data['gt_java_code']

        # split java_code by module 
        java_codes = split_java_code(java_code)
        java_codes = [unit['content'] for unit in java_codes if 'content' in unit]
        # split gt_java_code by module
        gt_java_codes = split_java_code(gt_java_code)
        gt_java_codes = [unit['content'] for unit in gt_java_codes if 'content' in unit]
        if len(java_codes) != len(gt_java_codes):
            print(f"⚠️  Module count mismatch: {len(java_codes)} vs {len(gt_java_codes)}")
            if len(gt_java_codes) < len(java_codes):
                # gt_java_codes가 부족한 경우, gt_java_codes를 java_codes의 길이에 맞춰서 채움
                gt_java_codes += [''] * (len(java_codes) - len(gt_java_codes))
            elif len(java_codes) < len(gt_java_codes):
                # java_codes가 부족한 경우, java_codes를 gt_java_codes의 길이에 맞춰서 채움
                java_codes += [''] * (len(gt_java_codes) - len(java_codes))

        print(f"🚀 Converting {len(java_codes)} Modules... (Module Mode)")

        for i, (java_module_code, gt_java_module_code) in enumerate(zip(java_codes, gt_java_codes)):
            print(f"\n{'='*60}")
            print(f"Converting module {i+1}/{len(java_codes)}")
            print(f"{'='*60}")
            
            try:
                contexts = self._build_contexts(contexts, java_module_code)

                result = self.convert_code(
                    contexts, java_module_code, gt_java_module_code
                )
                results.append(result)

            except Exception as e:
                print(f"❌ Error converting module {i+1}/{len(java_codes)}: {e}")
                results.append({
                    'module_code': java_module_code,
                    'error': str(e),
                    'is_correct': False
                })
        
        # 전체 결과 요약
        self._print_summary(results)
        
        return results

    def convert_whole_page(self, data: dict[str, any]) -> dict[str, any]:
        """전체 페이지 변환 (Page 단위)"""
        contexts = data['contexts']
        java_code = data['java_code']
        gt_java_code = data['gt_java_code']
        
        print(f"📄 Converting entire page... (Page Mode)")
        print(f"   Original code length: {len(java_code)} characters")

        contexts = self._build_contexts(contexts, java_code)

        result = self.convert_code(contexts, java_code, gt_java_code)

        self._print_page_summary(result)
        
        return result
    
    def _print_prompt_response(self, prompt: str, response: str, stage: str, parsed_code: str = None):
        """프롬프트, 응답, 파싱된 코드 출력"""
        print(f"\n{stage}:")
        print("Prompt:")
        print_color(prompt, "green")
        print()
        print("Response:")
        print_color(response, "cyan")
        print()
        
        if parsed_code is not None:
            # 새로운 색상 추가
            print("Parsed Code:")
            print_color(parsed_code, "magenta")
            print()

    def _evaluate_output(self, output: str, gt_code: str) -> dict:
        """출력 결과 평가 (페이지 단위, 다중 메트릭 포함)"""

        def remove_comments(code):
            # 라인 주석 + 블록 주석 제거
            code = re.sub(r'//.*?$', '', code, flags=re.MULTILINE)
            code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
            return code

        def contains_vo_method(code):
            return bool(re.search(r'\b(set|get)[A-Z]\w*\s*\(', code))

        def contains_map_ops(code):
            return bool(re.search(r'\bmap\.(get|put|remove)\s*\(', code, flags=re.IGNORECASE))

        result = {}

        # 1. Exact match (공백 무시)
        exact_match = matches_regardless_of_spacing(output, gt_code)
        result['exact_match'] = exact_match

        # 2. Comment-ignored match
        output_no_comments = remove_comments(output)
        gt_no_comments = remove_comments(gt_code)
        comment_ignored_match = matches_regardless_of_spacing(output_no_comments, gt_no_comments)
        result['comment_ignored_match'] = comment_ignored_match

        # 3. VO getter/setter 패턴 사용 여부
        vo_pattern_used = contains_vo_method(output)
        result['vo_pattern_used'] = vo_pattern_used

        # 4. Map 관련 코드 남아 있는지 여부
        map_pattern_remaining = contains_map_ops(output)
        result['map_pattern_remaining'] = map_pattern_remaining

        # 5. AST 구조 비교
        try:
            ast_output = get_ast(output_no_comments)
            ast_gt = get_ast(gt_no_comments)
            ast_match = ast_output == ast_gt
        except Exception as e:
            print(f"⚠️ AST parsing error: {e}")
            ast_match = False
        result['ast_match'] = ast_match

        # 6. 문자열 유사도
        similarity = SequenceMatcher(None, output.strip(), gt_code.strip()).ratio()
        result['similarity'] = similarity

        # 7. 최종 점수 계산
        score = 0
        score += 40 if exact_match else 0
        score += 20 if comment_ignored_match else 0
        score += 10 if vo_pattern_used else 0
        score += 10 if not map_pattern_remaining else 0
        score += 10 if ast_match else 0
        score += 10 * similarity  # similarity: 0~1
        final_score = min(100, round(score))
        result['final_score'] = final_score

        # 최종 요약 출력
        print(f"✅ Evaluation result:")
        for key, value in result.items():
            print(f"  {key}: {value}")

        return result
    
    def _print_summary(self, results: list[dict[str, any]]):
        """결과 요약 출력 (Module 모드)"""
        
        total = len(results)
        correct = sum(1 for r in results if r.get('is_correct', False))
        
        print(f"\n{'='*60}")
        print(f"📊 MODULE CONVERSION SUMMARY")
        print(f"{'='*60}")
        print(f"Total functions: {total}")
        print(f"Successful conversions: {correct}")
        print(f"Failed conversions: {total - correct}")
        print(f"Success rate: {correct/total*100:.1f}%" if total > 0 else "N/A")
        
        if total - correct > 0:
            print(f"\n❌ Failed functions:")
            for result in results:
                if not result.get('is_correct', False):
                    error = result.get('error', 'Incorrect output')
                    print(f"  - {error}")

    def _print_page_summary(self, result: dict[str, any]):
        """결과 요약 출력 (Page 모드)"""
        
        print(f"\n{'='*60}")
        print(f"📊 PAGE CONVERSION SUMMARY")
        print(f"{'='*60}")
        print(f"Conversion mode: {result.get('mode', 'page')}")
        print(f"Success: {'✅' if result.get('is_correct', False) else '❌'}")
        print(f"Iterations used: {result.get('iterations', 1)}")
        print(f"Original code length: {len(result.get('original_code', ''))}")
        print(f"Converted code length: {len(result.get('converted_code', ''))}")

    def convert_line_by_line(self, data: dict[str, any]) -> list[dict[str, any]]:
        """라인별 변환 (Line 단위)"""
        
        results = []
        contexts = data['contexts']
        java_code = data['java_code']
        gt_java_code = data['gt_java_code']
        
        # 코드를 라인별로 분할
        java_lines = java_code.splitlines()
        gt_java_lines = gt_java_code.splitlines() if gt_java_code else java_lines
        
        # GT 라인 수가 부족한 경우 빈 문자열로 채움
        if len(gt_java_lines) < len(java_lines):
            gt_java_lines += [''] * (len(java_lines) - len(gt_java_lines))
        elif len(java_lines) < len(gt_java_lines):
            java_lines += [''] * (len(gt_java_lines) - len(java_lines))

        print(f"📝 Converting {len(java_lines)} lines... (Line Mode)")

        for i, (line, gt_line) in enumerate(zip(java_lines, gt_java_lines)):
            print(f"\n{'='*60}")
            print(f"Converting line {i+1}/{len(java_lines)}")
            print(f"Original line: {line}")
            print(f"{'='*60}")
            
            # 빈 라인이나 주석만 있는 경우 건너뛰기 (옵션)
            if self.skip_non_map and (not line.strip() or line.strip().startswith('//')):
                print("ℹ️  Empty line or comment. Skipping conversion.")
                results.append({
                    'original_code': line,
                    'converted_code': line,
                    'is_correct': True,
                    'iterations': 0,
                    'ground_truth': gt_line,
                    'skipped': True
                })
                continue
            
            try:
                contexts = self._build_contexts(contexts, line)
                result = self.convert_code(contexts, line, gt_line)
                results.append(result)

            except Exception as e:
                print(f"❌ Error converting line {i+1}/{len(java_lines)}: {e}")
                results.append({
                    'original_code': line,
                    'error': str(e),
                    'is_correct': False,
                    'ground_truth': gt_line
                })
        
        # 전체 결과 요약
        self._print_line_summary(results)
        
        return results

    def _print_line_summary(self, results: list[dict[str, any]]):
        """결과 요약 출력 (Line 모드)"""
        
        total = len(results)
        correct = sum(1 for r in results if r.get('is_correct', False))
        skipped = sum(1 for r in results if r.get('skipped', False))
        
        print(f"\n{'='*60}")
        print(f"📊 LINE CONVERSION SUMMARY")
        print(f"{'='*60}")
        print(f"Total lines: {total}")
        print(f"Successful conversions: {correct}")
        print(f"Failed conversions: {total - correct}")
        print(f"Skipped lines: {skipped}")
        print(f"Success rate: {correct/total*100:.1f}%" if total > 0 else "N/A")
        
        if total - correct > 0:
            print(f"\n❌ Failed lines:")
            failed_count = 0
            for i, result in enumerate(results):
                if not result.get('is_correct', False) and not result.get('skipped', False):
                    failed_count += 1
                    if failed_count <= 5:  # 처음 5개만 표시
                        error = result.get('error', 'Incorrect output')
                        original = result.get('original_code', '')[:50]
                        print(f"  - Line {i+1}: {original}... | Error: {error}")
                    elif failed_count == 6:
                        print(f"  - ... and {total - correct - 5} more failed lines")


def create_parser():
    """argparse 파서 생성"""
    parser = argparse.ArgumentParser(
        description="Map-based implementation을 VO-based implementation으로 변환",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  %(prog)s                                    # 기본 변환 (module 모드, 모든 함수)
  %(prog)s --mode module --use-diff           # Module 모드 + Diff 정보 포함
  %(prog)s --mode page --use-reflextion       # Page 모드 + 피드백 기반 개선
  %(prog)s --mode page --use-diff --use-reflextion    # Page 모드 + Diff + 피드백
  %(prog)s --mode page --use-api-rag    # Page 모드 + RAG 사용
  %(prog)s --context sample_input.txt --java Sample.java --iterations 5
        """
    )
    
    parser.add_argument(
        '--model',
        type=str,
        default='qwen2.5-coder:7b',
        help='사용할 모델 지정 (기본: qwen2.5-coder:7b)'
    )
    
    parser.add_argument(
        '--mode',
        choices=['module', 'page', 'line'],
        default='module',
        help='변환 모드 선택: module (함수별 변환), page (전체 페이지 변환), 또는 line (라인별 변환) (기본: module)'
    )
    
    parser.add_argument(
        '--use-diff',
        action='store_true',
        help='변환 시 diff 정보 포함'
    )
    
    parser.add_argument(
        '--use-reflextion',
        action='store_true',
        help='피드백 기반 반복 개선 사용'
    )

    parser.add_argument(
        '--use-prompt-normalization',
        action='store_true',
        help='프롬프트 정규화 사용'
    )

    parser.add_argument(
        '--use-prefix-output',
        action='store_true',
        # default=True,
        help='출력 프롬프트에 ```java 코드 블록 사용 (기본: True)'
    )

    parser.add_argument(
        '--use-vo-generator',
        action='store_true',
        help='VO 생성기 사용'
    )

    parser.add_argument(
        '--vo-package',
        type=str,
        default=None,
        help='VO 파일 경로'
    )

    parser.add_argument(
        '--vo-class-name',
        type=str,
        default=None,
        help='VO 클래스 이름'
    )

    parser.add_argument(
        '--project-root',
        type=str,
        default=None,
        help='프로젝트 루트 경로'
    )

    parser.add_argument(
        '--vo-file',
        type=str,
        default=None,
        help='VO 파일 경로'
    )

    parser.add_argument(
        '--use-api-rag',
        action='store_true',
        help='Proworks5 api RAG 사용'
    )

    parser.add_argument(
        '--use-case-rag',
        action='store_true',
        help='Case RAG 사용'
    )
    
    parser.add_argument(
        '--max-line-limit-offset', '-mlo',
        type=int,
        default=None,
        help='Agent 응답 라인 수 제한을 위한 오프셋 (None=제한 없음, 기본: None)'
    )
    
    parser.add_argument(
        '--skip-non-map',
        action='store_true',
        help='Map 관련 코드가 없는 경우 변환 건너뛰기'
    )
    
    parser.add_argument(
        '--context',
        type=str,
        # default="reflexion_poc/sample/sample_input.txt",
        # default="data/samples/vo.txt",
        default=None,
        help='컨텍스트 파일 경로 (기본: reflexion_poc/sample/sample_input.txt)'
    )
    
    parser.add_argument(
        '--java',
        type=str,
        default="data/samples/file_sample_original/SampleTaskServiceImpl_in.java",
        help='입력 Java 파일 경로'
    )
    
    parser.add_argument(
        '--gt',
        type=str,
        default="data/samples/file_sample_original/SampleTaskServiceImpl_out.java",
        help='Ground truth Java 파일 경로 (기본: 입력 파일과 동일)'
    )

    parser.add_argument(
        '--iterations', '-i',
        type=int,
        default=1,
        help='최대 반복 횟수 (기본: 1)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='상세 출력 모드'
    )
    
    return parser


def run_conversion(config: ConversionConfig) -> str | None:
    """변환 실행 함수
    
    Returns:
        str | None: 변환된 코드 (오류 발생시 None 반환)
    """
    try:
        # 파일 경로 설정
        context_path = config.context
        input_java_path = config.java
        gt_java_path = config.gt or input_java_path  # gt가 없으면 입력 파일 사용

        # 변환기 초기화
        converter = AIConverter(
            agent=Agent(config.model, verbose=config.verbose),
            use_diff=config.use_diff,
            use_reflextion=config.use_reflextion,
            use_prompt_normalization=config.use_prompt_normalization,
            use_prefix_output=config.use_prefix_output,
            use_vo_generator=config.use_vo_generator,
            vo_file=config.vo_file,
            use_api_rag=config.use_api_rag,
            use_case_rag=config.use_case_rag,
            iterations=config.iterations,
            skip_non_map=config.skip_non_map,
            max_line_limit_offset=config.max_line_limit_offset,
            project_root=config.project_root,
            vo_package=config.vo_package,
            vo_class_name=config.vo_class_name
        )
        
        # 파일 로드
        if config.verbose:
            print("📁 Loading files...")
            print(f"  Context: {context_path}")
            print(f"  Java: {input_java_path}")
            print(f"  GT: {gt_java_path}")
            print(f"  Mode: {config.mode}")
        
        data = converter.load_java_files(input_java_path, context_path, gt_java_path)
        
        # 모드에 따른 변환 실행
        if config.mode == 'module':
            print(f"🚀 Converting all Module... (Module Mode)")
            results = converter.convert_all_modules(data)
            
            print(f"\n🎉 Module conversion completed!")
            
            # 결과 요약
            if len(results) > 1:
                successful = sum(1 for r in results if r.get('is_correct', False))
                print(f"📊 Success rate: {successful}/{len(results)} ({successful/len(results)*100:.1f}%)")
            
            # 모든 모듈의 변환된 코드를 합치기
            converted_codes = []
            for result in results:
                converted_codes.append(result.get('converted_code'))
            
            return '\n\n'.join(converted_codes)
                
        elif config.mode == 'page':
            print(f"📄 Converting entire page... (Page Mode)")
            result = converter.convert_whole_page(data)
            
            print(f"\n🎉 Page conversion completed!")
            
            # 결과 요약
            converter._print_page_summary(result)
            
            return result.get('converted_code')
        
        elif config.mode == 'line':
            print(f"📝 Converting line by line... (Line Mode)")
            results = converter.convert_line_by_line(data)
            
            print(f"\n🎉 Line-by-line conversion completed!")
            
            # 결과 요약
            if len(results) > 1:
                successful = sum(1 for r in results if r.get('is_correct', False))
                print(f"📊 Success rate: {successful}/{len(results)} ({successful/len(results)*100:.1f}%)")
            
            # 모든 라인의 변환된 코드를 합치기
            converted_lines = []
            for result in results:
                converted_lines.append(result.get('converted_code'))
            
            return '\n'.join(converted_lines)
        
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        print("💡 Make sure the required files exist:")
        print(f"  - Context: {config.context}")
        print(f"  - Input Java: {config.java}")
        return None
        
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        if config.verbose:
            import traceback
            traceback.print_exc()
        return None


def main():
    """메인 실행 함수"""
    # argparse 설정
    parser = create_parser()
    args = parser.parse_args()
    
    # argparse Namespace를 pydantic 모델로 변환 (자동 유효성 검사 포함)
    config = ConversionConfig(**vars(args))
    
    # 변환 실행 및 결과 반환
    result = run_conversion(config)
    
    return result


if __name__ == "__main__":
    main()