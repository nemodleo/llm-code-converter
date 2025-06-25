from difflib import unified_diff
from typing import Any
import re

from agent import Agent
from convertor import Convertor
from task import TaskConfig


class ApplyModel:
    def __init__(self, task_type: str = "map_to_vo"):
        self.language = "java"
        self.task_config = TaskConfig.get_task_config(task_type)
        
        # Task-aware Diff 처리 전문 Agent  
        self.diff_enhancer = Agent(
            model='llama3.2',
            system_prompt=self._get_system_prompt()
        )

    def apply(self, original_lines: list[str], convertor_result: dict[str, Any]) -> list[str]:
        """
        Enhanced diff-based transformation pipeline:
        1. Use conversion result from Convertor class
        2. Generate intent-aware enhanced diff
        3. Apply enhanced diff to original code
        """
        
        # 변환 결과에서 정보 추출
        converted_code = convertor_result['converted_code']
        conversion_intent = convertor_result['intent']
        
        modified_lines = converted_code.split('\n')
        
        print(f"🧩🔍 Generating {self.task_config['name']} enhanced diff...")
        print(f"Task: {self.task_config['description']}")
        print(f"Transformation purpose: {conversion_intent.get('main_purpose', 'Unknown')}")
        print(f"Scope: {conversion_intent.get('transformation_scope', 'Unknown')}")
        print(f"Risk level: {conversion_intent.get('risk_level', 'Unknown')}")
        
        # Task-specific enhanced diff 생성
        enhanced_diff = self._generate_enhanced_diff(
            original_lines=original_lines,
            modified_lines=modified_lines,
            conversion_intent=conversion_intent
        )
        
        print("Enhanced diff:")
        print(enhanced_diff)
        
        # Enhanced diff 적용
        print("\n🛠 Applying enhanced diff...")
        result = self._apply_unified_diff(original_lines, enhanced_diff)
        
        return result

    def _generate_enhanced_diff(self, original_lines: list[str], modified_lines: list[str], 
                              conversion_intent: dict[str, Any]) -> str:
        """Generate task-specific enhanced diff using transformation intent"""
        
        # 기본 unified diff 생성
        base_diff = self._generate_unified_diff(original_lines, modified_lines)
        
        # Task-specific domain knowledge
        domain_knowledge = self.task_config['domain_knowledge']
        enhancement_rules = self.task_config['enhancement_rules']
        quality_checks = self.task_config['quality_checks']
        
        prompt = f"""
Generate an enhanced unified diff for {self.task_config['name']} based on the base diff and comprehensive transformation intent.

**TASK CONTEXT:**
Task: {self.task_config['name']}
Description: {self.task_config['description']}
Purpose: {domain_knowledge['purpose']}

**DOMAIN EXPERTISE - {self.task_config['name'].upper()}:**
Key Benefits:
{chr(10).join('- ' + benefit for benefit in domain_knowledge['benefits'])}

Common Transformation Patterns:
{chr(10).join('- ' + pattern for pattern in domain_knowledge['common_transformations'])}

Code Patterns to Recognize:
- Map Usage: {domain_knowledge['patterns']['map_usage']}
- VO Replacement: {domain_knowledge['patterns']['vo_replacement']}
- Getter Pattern: {domain_knowledge['patterns']['getter_pattern']} → {domain_knowledge['patterns']['vo_access']}

**TRANSFORMATION METADATA:**
Purpose: {conversion_intent.get('main_purpose', 'Unknown')}
Scope: {conversion_intent.get('transformation_scope', 'moderate')}
Risk Level: {conversion_intent.get('risk_level', 'medium')}

Specific Changes:
{chr(10).join('- ' + change for change in conversion_intent.get('specific_changes', []))}

Preservation Rules:
{chr(10).join('- ' + rule for rule in conversion_intent.get('preservation_rules', []))}

Enhancement Opportunities:
{chr(10).join('- ' + opportunity for opportunity in conversion_intent.get('enhancement_opportunities', []))}

**BASE UNIFIED DIFF:**
```diff
{base_diff}
```

**TASK-SPECIFIC ENHANCEMENT DIRECTIVES:**
Apply the following {self.task_config['name']} optimizations:

1. 🔍 SYNTAX & TYPE SAFETY: 
   - Fix missing semicolons, brace matching, import organization
   - Ensure proper type declarations for VO fields
   - Add generic type parameters where needed

2. 🧹 CODE FORMATTING & CONVENTIONS:
   - Apply consistent indentation, spacing, Java style conventions
   - Field Naming: {enhancement_rules['field_naming']}
   - Type Inference: {enhancement_rules['type_inference']}

3. 💡 INTELLIGENT COMPLETION:
   - Convert TODO comments to proper VO implementation
   - Validation: {enhancement_rules['validation']}
   - Immutability: {enhancement_rules['immutability']}

4. 🚫 CODE OPTIMIZATION:
   - Remove redundant Map operations
   - Eliminate unnecessary type casting
   - Clean up unused imports and variables

5. 🎯 TASK-SPECIFIC QUALITY ASSURANCE:
{chr(10).join('   - ' + check for check in quality_checks)}

**CRITICAL CONSTRAINTS:**
- Generate ONLY ONE clean, complete unified diff block
- Deletion lines (-) may only be modified if explicitly required by transformation intent
- Addition lines (+) should incorporate all relevant task-specific enhancement opportunities
- Maintain strict unified diff format compliance with single @@ header
- Never compromise the core Map-to-VO transformation objectives
- Respect preservation rules absolutely
- Apply domain expertise to ensure high-quality VO implementation
- Ensure generated code compiles without errors
- Use proper Java syntax for all transformations
- Do NOT generate multiple diff blocks or fragmented diffs

Generate only ONE complete enhanced unified diff using ```diff``` tags:
"""
        
        response = self.diff_enhancer(prompt)
        
        # diff 블록 추출
        diff_match = re.search(r'```diff\n(.*?)\n```', response, re.DOTALL)
        if diff_match:
            print("✅ Task-specific enhanced diff generated successfully")
            return diff_match.group(1).strip()
        else:
            print("⚠️ Enhanced diff generation failed, using base diff")
            return base_diff

    def _generate_unified_diff(self, original_lines: list[str], modified_lines: list[str]) -> str:
        """Generate standard unified diff"""
        diff_lines = list(unified_diff(
            original_lines,
            modified_lines,
            fromfile='original.java',
            tofile='modified.java',
            lineterm=''
        ))
        return '\n'.join(diff_lines)

    def _apply_unified_diff(self, original_lines: list[str], diff_content: str) -> list[str]:
        """Apply enhanced unified diff to original code with improved parsing"""
        
        # diff 파싱 - 여러 diff 블록 처리
        diff_lines = diff_content.split('\n')
        
        # 모든 @@ 헤더 찾기
        header_indices = []
        for i, line in enumerate(diff_lines):
            if line.startswith('@@'):
                header_indices.append(i)
        
        if not header_indices:
            print("⚠️ No diff headers found, returning original code")
            return original_lines
        
        # 첫 번째 diff 블록만 사용 (가장 완전한 것으로 가정)
        start_idx = header_indices[0] + 1
        end_idx = header_indices[1] if len(header_indices) > 1 else len(diff_lines)
        
        print(f"🔧 Using diff block from line {start_idx} to {end_idx}")
        
        # diff 적용
        result = []
        orig_idx = 0
        
        for line in diff_lines[start_idx:end_idx]:
            if not line.strip():  # 빈 라인 스킵
                continue
                
            if line.startswith(' '):  # 변경되지 않은 라인
                if orig_idx < len(original_lines):
                    result.append(original_lines[orig_idx])
                    orig_idx += 1
                    
            elif line.startswith('-'):  # 삭제된 라인
                orig_idx += 1  # 원본에서 스킵
                
            elif line.startswith('+'):  # 추가된 라인
                result.append(line[1:])  # '+' 제거하고 추가
        
        # 남은 원본 라인들 추가
        while orig_idx < len(original_lines):
            result.append(original_lines[orig_idx])
            orig_idx += 1
        
        return result

    def _get_system_prompt(self):
        """Expert-crafted system prompt for task-specific enhanced diff generation"""
        
        task_name = self.task_config['name']
        domain_knowledge = self.task_config['domain_knowledge']
        
        return f"""You are an elite {task_name} specialist with advanced unified diff enhancement capabilities.

SPECIALIZED DOMAIN EXPERTISE - {task_name.upper()}:
- Master-level understanding of {task_name} patterns and best practices
- Deep knowledge of Java enterprise patterns and type-safe design principles
- Expert in Map-to-VO transformation patterns and modern Java development
- Advanced understanding of immutable object design and data encapsulation

TASK-SPECIFIC TECHNICAL KNOWLEDGE:
Purpose: {domain_knowledge['purpose']}
Key Benefits Understanding:
{chr(10).join('- ' + benefit for benefit in domain_knowledge['benefits'])}

Transformation Patterns Mastery:
{chr(10).join('- ' + pattern for pattern in domain_knowledge['common_transformations'])}

ENHANCEMENT METHODOLOGY:
- Apply {task_name} domain expertise with surgical precision
- Recognize Map usage patterns and convert to appropriate VO structures
- Generate type-safe, immutable Value Objects following Java best practices
- Maintain absolute fidelity to unified diff format standards
- Apply enhancements that amplify Map-to-VO transformation objectives

QUALITY ASSURANCE FOR {task_name.upper()}:
- Ensure complete Map elimination and VO implementation
- Verify type safety and immutability principles
- Validate proper field naming and access patterns
- Apply conservative enhancement strategies to minimize risk
- Generate diffs that are semantically correct and follow enterprise Java patterns

OPTIMIZATION PRINCIPLES:
- Enhance only within the scope of Map-to-VO transformation intent
- Prioritize type safety, immutability, and enterprise Java standards
- Apply domain-specific best practices without overstepping transformation boundaries
- Generate enhancements that experienced Java enterprise developers would naturally apply

You excel at understanding Map-to-VO transformation requirements and generating enhanced diffs that create high-quality, type-safe Value Objects while maintaining absolute safety and precision.

CRITICAL DIFF GENERATION RULES:
- Generate EXACTLY ONE unified diff block with single @@ header
- Ensure all generated code compiles and follows Java syntax rules
- Apply Map-to-VO transformations with complete accuracy
- Never generate fragmented or multiple diff blocks
- Maintain logical consistency throughout the transformation"""

    # 기존과 동일한 인터페이스 (호환성)
    def diff(self, original_lines: list[str], modified_lines: list[str]) -> list[str]:
        """Legacy compatibility method (unused)"""
        return []


def test_map_to_vo_transformation():
    """Test ApplyModel with Map-to-VO transformation"""
    
    # Map 기반 코드 예제
    original = [
        "public class UserService {",
        "    private Map<String, Object> userData;",
        "    ",
        "    public UserService() {",
        "        this.userData = new HashMap<>();",
        "    }",
        "    ",
        "    public void createUser(String name, String email, Integer age) {",
        "        userData.put(\"name\", name);",
        "        userData.put(\"email\", email);", 
        "        userData.put(\"age\", age);",
        "        userData.put(\"created_at\", System.currentTimeMillis());",
        "    }",
        "    ",
        "    public String getUserInfo() {",
        "        String name = (String) userData.get(\"name\");",
        "        String email = (String) userData.get(\"email\");",
        "        Integer age = (Integer) userData.get(\"age\");",
        "        return name + \" (\" + email + \"), Age: \" + age;",
        "    }",
        "    ",
        "    public boolean isAdult() {",
        "        Integer age = (Integer) userData.get(\"age\");",
        "        return age != null && age >= 18;",
        "    }",
        "}"
    ]
    
    print("🗺️ ORIGINAL CODE (Map-based):")
    for i, line in enumerate(original, 1):
        print(f"{i:2d}: {line}")
    
    # Convertor 사용 (Map-to-VO 변환 요청)
    convertor = Convertor(task_type="map_to_vo")
    conversion_result = convertor.convert_with_intent(
        '\n'.join(original), 
        "Convert Map-based userData to a proper UserVO class with immutable fields, type safety, and proper getters. Replace all Map operations with VO usage."
    )
    
    print(f"\n🔄 CONVERSION INTENT:")
    print(f"Purpose: {conversion_result['intent']['main_purpose']}")
    print(f"Changes: {conversion_result['intent']['specific_changes']}")
    
    # Map-to-VO 전용 ApplyModel 사용
    apply_model = ApplyModel(task_type="map_to_vo")
    result = apply_model.apply(original, conversion_result)
    
    print("\n📋 FINAL RESULT (VO-based):")
    for i, line in enumerate(result, 1):
        print(f"{i:2d}: {line}")


if __name__ == "__main__":
    test_map_to_vo_transformation()
