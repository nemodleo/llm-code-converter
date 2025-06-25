import re

from aiconvertor.task import TaskConfig


class PromptHandler:
    """Task별 프롬프트 생성기"""
    
    def __init__(self, task_type: str = "map_to_vo"):
        """
        Args:
            task_type: 프롬프트를 생성할 task 타입 (기본값: "map_to_vo")
        """
        self.task_type = task_type
        self.task_config = TaskConfig.get_task_config(task_type)
        self.rules = self.task_config.get("rules", {})
    
    def build_initial_prompt(self, 
                             contexts: str,
                             code: str,
                             prefix_output: str = "") -> str:
        """초기 변환 프롬프트 생성"""
        
        rules = self.rules.get("initial", "")
        if not rules:
            raise ValueError(f"No rules found for task type: {self.task_type}")

        prompt_parts = [contexts]
        prompt_parts.append(f"<rules>\n{rules}\n</rules>")
        prompt_parts.append(f"Input: ```java\n{code}\n```")
        if prefix_output:
            prompt_parts.append(f"Output: {prefix_output}")
        else:
            prompt_parts.append("Output:")
        prompt = "\n\n".join(prompt_parts).strip()

        return prompt
    
    def build_feedback_prompt(self,
                              contexts: str,
                              candidate_code: str,
                              diff_text: str = None,
                              use_diff: bool = False) -> str:
        """피드백 생성 프롬프트 생성"""
        
        feedback = self.rules.get("feedback", "")
        if not feedback:
            raise ValueError(f"No feedback found for task type: {self.task_type}")

        prompt_parts = [contexts]
        prompt_parts.append(f"<candidate>\n{candidate_code}\n</candidate>")
        if use_diff and diff_text:
            prompt_parts.append(f"<diff>\n{diff_text}\n</diff>")
        prompt_parts.append(feedback)
        prompt = "\n\n".join(prompt_parts).strip()

        return prompt
    
    def build_correction_prompt(self,
                                contexts: str,
                                candidate_code: str,
                                code: str,
                                feedback: str = None,
                                diff_text: str = None,
                                use_diff: bool = False,
                                prefix_output: str = "") -> str:
        """수정 프롬프트 생성"""
        
        correction = self.rules.get("correction", "")
        if not correction:
            raise ValueError(f"No correction found for task type: {self.task_type}")

        prompt_parts = [contexts]
        prompt_parts.append(f"<candidate>\n{candidate_code}\n</candidate>")
        if use_diff and diff_text:
            prompt_parts.append(f"<diff>\n{diff_text}\n</diff>")
        if feedback:
            prompt_parts.append(f"<feedback>\n{feedback}\n</feedback>")
        prompt_parts.append(correction)
        prompt_parts.append(f"Input: ```java\n{code}\n```")
        if prefix_output:
            prompt_parts.append(f"Output: {prefix_output}")
        else:
            prompt_parts.append("Output:")
        prompt = "\n\n".join(prompt_parts).strip()

        return prompt

    def get_task_info(self) -> dict:
        """현재 task의 정보 반환"""
        return {
            "task_type": self.task_type,
            "name": self.task_config.get("name", ""),
            "description": self.task_config.get("description", ""),
            "available_templates": list(self.rules.keys())
        }
    
    def extract_code_from_response(self, response: str, use_prefix_output: bool = True) -> str:
        """응답에서 코드 블록 추출"""
        # ```java {code}``` or ```{code}```
        matches = re.findall(r"```(?:java)?\s*([\s\S]*?)\s*```", response)

        # {code}``` caused by prefix output formatting
        if len(matches) == 0 and use_prefix_output:
            matches = re.findall(r"([\s\S]*?)\s*```", response)

        # ```java {code}``` or ```{code} caused by max line limit offset
        if len(matches) == 0 or matches == [""]:
            matches = re.findall(r"```(?:java)?\s*([\s\S]*)", response)

        # no matches: 전체 응답 반환
        if len(matches) == 0 or matches == [""]:
            return response.strip()

        code = ""
        for match in matches:
            if match.strip() == "":
                continue
            code = match.strip()
            break

        return code
    
    def extract_feedback_from_response(self, response: str) -> str:
        """응답에서 피드백 추출"""
        
        # 코드 블록 제거
        feedback = response.strip()
        feedback = feedback.strip("```java").strip("```")
        
        return feedback.strip()


# 편의 함수들
def load_contexts(file_path: str) -> str:
    """파일에서 전체 컨텍스트 로드"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Context file not found: {file_path}")
    except Exception as e:
        raise RuntimeError(f"Failed to load context file: {e}")


def create_task_prompt_builder(task_type: str = "map_to_vo") -> PromptHandler:
    """지정된 task 타입에 대한 PromptHandler 생성"""
    return PromptHandler(task_type)


def create_basic_map_to_vo_prompt(contexts: str, 
                                function_name: str,
                                function_signature: str) -> str:
    """Map-to-VO 변환을 위한 기본 프롬프트 생성 (하위 호환성)"""
    
    builder = PromptHandler("map_to_vo")
    return builder.build_module_initial_prompt(contexts, function_name, function_signature)


def create_feedback_prompt(contexts: str,
                         candidate_code: str,
                         use_diff: bool = False,
                         diff_text: str = None,
                         task_type: str = "map_to_vo") -> str:
    """피드백 프롬프트 생성 (하위 호환성)"""
    
    builder = PromptHandler(task_type)
    return builder.build_module_feedback_prompt(
        contexts, candidate_code, diff_text, use_diff
    )


def create_correction_prompt(contexts: str,
                           candidate_code: str,
                           feedback: str,
                           function_name: str,
                           function_signature: str,
                           use_diff: bool = False,
                           diff_text: str = None,
                           task_type: str = "map_to_vo") -> str:
    """수정 프롬프트 생성 (하위 호환성)"""
    
    builder = PromptHandler(task_type)
    return builder.build_module_correction_prompt(
        contexts, candidate_code, 
        function_name, function_signature, feedback, diff_text, use_diff
    )


# 새로운 module/page 전용 편의 함수들
def create_module_initial_prompt(contexts: str,
                               function_name: str,
                               function_signature: str,
                               task_type: str = "map_to_vo") -> str:
    """Module 초기 변환 프롬프트 생성"""
    
    builder = PromptHandler(task_type)
    return builder.build_module_initial_prompt(contexts, function_name, function_signature)


def create_module_feedback_prompt(contexts: str,
                                candidate_code: str,
                                use_diff: bool = False,
                                diff_text: str = None,
                                task_type: str = "map_to_vo") -> str:
    """Module 피드백 프롬프트 생성"""
    
    builder = PromptHandler(task_type)
    return builder.build_module_feedback_prompt(
        contexts, candidate_code, diff_text, use_diff
    )


def create_module_correction_prompt(contexts: str,
                                  candidate_code: str,
                                  function_name: str,
                                  function_signature: str,
                                  feedback: str = None,
                                  use_diff: bool = False,
                                  diff_text: str = None,
                                  task_type: str = "map_to_vo") -> str:
    """Module 수정 프롬프트 생성"""
    
    builder = PromptHandler(task_type)
    return builder.build_module_correction_prompt(
        contexts, candidate_code, 
        function_name, function_signature, feedback, diff_text, use_diff
    )


def create_page_initial_prompt(contexts: str,
                             page_code: str,
                             task_type: str = "map_to_vo") -> str:
    """Page 초기 변환 프롬프트 생성"""
    
    builder = PromptHandler(task_type)
    return builder.build_page_initial_prompt(contexts, page_code)


def create_page_feedback_prompt(contexts: str,
                              candidate_page: str,
                              use_diff: bool = False,
                              diff_text: str = None,
                              task_type: str = "map_to_vo") -> str:
    """Page 피드백 프롬프트 생성"""
    
    builder = PromptHandler(task_type)
    return builder.build_page_feedback_prompt(
        contexts, candidate_page, diff_text, use_diff
    )


def create_page_correction_prompt(contexts: str,
                                candidate_page: str,
                                feedback: str = None,
                                use_diff: bool = False,
                                diff_text: str = None,
                                task_type: str = "map_to_vo") -> str:
    """Page 수정 프롬프트 생성"""
    
    builder = PromptHandler(task_type)
    return builder.build_page_correction_prompt(
        contexts, candidate_page, feedback, diff_text, use_diff
    )


if __name__ == "__main__":
    # 테스트 코드
    print("🔍 Testing PromptHandler with different task types")
    
    # Map-to-VO task 테스트
    map_builder = PromptHandler("map_to_vo")
    print(f"✅ Map-to-VO Builder: {map_builder.get_task_info()}")
    
    # Legacy API modernization task 테스트
    legacy_builder = PromptHandler("legacy_api_modernization")
    print(f"✅ Legacy API Builder: {legacy_builder.get_task_info()}")
    
    # 테스트 데이터
    test_context = "public class TestClass { /* context */ }"
    test_function = "testMethod"
    test_signature = "public void testMethod(Map<String, Object> data)"
    test_candidate = "public void testMethod(TestVO data) { /* implementation */ }"
    test_feedback = "✅ Method name unchanged\n❌ Missing null check"
    
    # Map-to-VO 초기 프롬프트 테스트
    try:
        initial_prompt = map_builder.build_module_initial_prompt(
            test_context, test_function, test_signature
        )
        print("\n🔍 Map-to-VO Initial Prompt:")
        print(initial_prompt[:200] + "...")
    except Exception as e:
        print(f"❌ Map-to-VO test failed: {e}")
    
    # Legacy API 초기 프롬프트 테스트
    try:
        legacy_prompt = legacy_builder.build_module_initial_prompt(
            test_context, test_function, test_signature
        )
        print("\n🔍 Legacy API Initial Prompt:")
        print(legacy_prompt[:200] + "...")
    except Exception as e:
        print(f"❌ Legacy API test failed: {e}")
    
    print("\n✅ PromptHandler task separation test completed")