from typing import Any


class TaskConfig:
    """Task-specific configuration for different code transformation types"""
    
    @staticmethod
    def get_task_config(task_type: str) -> dict[str, Any]:
        """Get configuration for specific transformation task"""
        
        tasks = {
            "map_to_vo": {
                "name": "Map to VO Conversion",
                "description": "Convert Map-based data structures to Value Object (VO) classes",
                "rules": {
                    "initial": """
Given a previous implementation code, a reference Value Object class, and some additional previous context sources, rewrite the previous implementation to migrate from Map-based implementation to VO(Value Object)-based implementation, using the reference VO class provided whenever necessary.
Follow these rules exactly:
* Do NOT add, remove, or alter any comments.
* Keep method and parameter names unchanged.
* Keep all function and call names unchanged.
* Only change types (parameter, return, local) and the argument passed to calls.
* If the function implementation is using Map, convert it to use VO.
* The function implementation should behave the same as the original implementation.
Write your converted implementation in the `Previous implementation (to convert to VO-based implementation)`.
No extra text other than the code.
""".strip(),
                    "feedback": """
Given a previous implementation code, a reference Value Object class, and some additional previous context sources, <candidate> is the rewritten previous implementation to migrate from Map-based implementation to VO(Value Object)-based implementation, using the reference VO class provided.
Now your role is to check whether candidate satisfies these conditions:
* Do NOT add, remove, or alter any comments.
* Keep method and parameter names unchanged.
* Keep all function and call names unchanged.
* Only change types (parameter, return, local) and the argument passed to calls.
* If the function implementation is using Map, convert it to use VO.
* The function implementation should behave the same as the original implementation.
For each point, specify <✅ or ❌> and give a detailed feedback (and also provide the code snippet that needs improvement).

Output only feedback. No Java code output.
""".strip(),
                    "correction": """
Given a previous implementation code, a reference Value Object class, and some additional previous context sources, <candidate> is the rewritten previous implementation to migrate from Map-based implementation to VO(Value Object)-based implementation, using the reference VO class provided.
Rewrite the previous implementation to migrate from Map-based implementation to VO(Value Object)-based implementation, using the reference VO class provided whenever necessary.
Follow these rules exactly:
* Do NOT add, remove, or alter any comments.
* Keep method and parameter names unchanged.
* Keep all function and call names unchanged.
* Only change types (parameter, return, local) and the argument passed to calls.
* If the function implementation is using Map, convert it to use VO.
* The function implementation should behave the same as the original implementation.
Write your converted implementation in the `Previous implementation (to convert to VO-based implementation)`.
No extra text other than the code.
""".strip()
                },
                "incontext_config": {
                    "system_prompt": """You are an expert Java developer specializing in Map-to-VO conversions.

TASK: Convert data mapping operations to Value Object patterns.

INSTRUCTIONS:
1. Identify Map-based data access patterns in the input
2. Convert to appropriate Value Object field access
3. Maintain all business logic and validation
4. Follow the conversion patterns shown in examples
5. Ensure type safety and null handling

CONVERSION PRINCIPLES:
- Replace map.get("key") with vo.getField()
- Replace map.put("key", value) with vo.setField(value)
- Maintain data validation and business rules
- Preserve error handling and edge cases
""",
                    "example_templates": {
                        "simple": """Example {number}:
Input:  {input_line}
Output: {output_line}
""",
                        "with_context": """Example {number}:
Context (before):
{context_before}
Input:  {input_line}
Output: {output_line}
Context (after):
{context_after}
""",
                        "with_explanation": """Example {number} (similarity: {similarity:.2f}):
Input:  {input_line}
Output: {output_line}
Explanation: {explanation}
""",
                        "detailed": """Example {number}:
Context (before):
{context_before}
Input:  {input_line}
Output: {output_line}
Context (after):
{context_after}
Pattern: {pattern_type}
Note: {note}
"""
                    },
                    "instruction_templates": {
                        "basic": """CONVERT THE FOLLOWING:

{context_section}Input:  {query_line}
{context_after_section}Output: """,
                        "with_reasoning": """CONVERT THE FOLLOWING:

{context_section}Input:  {query_line}
{context_after_section}
REASONING STEPS:
1. Pattern Analysis: What type of code pattern is this?
2. Example Matching: Which reference example is most similar?
3. Transformation Rule: What conversion rule should be applied?
4. Output Generation: Apply the rule to generate the converted line.

Think step by step, then provide the final converted line.

Output: """,
                        "chain_of_thought": """CONVERT THE FOLLOWING:

{context_section}Input:  {query_line}
{context_after_section}
Let me work through this step by step:

1. Pattern Analysis: """,
                        "zero_shot": """CONVERT THE FOLLOWING:

No reference examples available. Apply general Java conversion principles:
- Convert Map operations to Value Object field access
- Maintain original functionality and variable names
- Follow Java naming conventions and best practices

{context_section}Input:  {query_line}
{context_after_section}Output: """
                    }
                },
                "domain_knowledge": {
                    "purpose": "Replace dynamic Map structures with type-safe, immutable Value Objects",
                    "benefits": [
                        "Type safety at compile time",
                        "Better IDE support and code completion",
                        "Immutable data structures",
                        "Clear API contracts",
                        "Reduced runtime errors"
                    ],
                    "patterns": {
                        "map_usage": "Map<String, Object> data = new HashMap<>();",
                        "vo_replacement": "UserVO user = new UserVO(name, email, age);",
                        "getter_pattern": "data.get(\"fieldName\")",
                        "setter_pattern": "data.put(\"fieldName\", value)",
                        "vo_access": "user.getFieldName()"
                    },
                    "common_transformations": [
                        "Extract Map keys as VO field names",
                        "Infer field types from Map usage patterns",
                        "Generate immutable VO classes with getters",
                        "Replace Map.get() calls with VO getter methods",
                        "Replace Map.put() calls with VO constructor parameters",
                        "Add proper validation and null checks"
                    ]
                },
                "enhancement_rules": {
                    "field_naming": "Convert snake_case or camelCase keys to proper Java field names",
                    "type_inference": "Infer appropriate Java types from Map value usage",
                    "validation": "Add @NonNull annotations and validation where appropriate",
                    "immutability": "Generate immutable VOs with final fields",
                    "builder_pattern": "Consider Builder pattern for complex VOs",
                    "serialization": "Add serialization annotations if needed"
                },
                "quality_checks": [
                    "Ensure all Map accesses are converted to VO methods",
                    "Verify type consistency across transformations",
                    "Check for proper null handling",
                    "Validate field name conventions",
                    "Ensure immutability principles"
                ]
            },

            "legacy_api_modernization": {
                "name": "Legacy API Modernization", 
                "description": "Modernize legacy API patterns to current Java standards",
                "prompt_templates": {
                    "basic_prompt": """
Given a previous implementation code and additional context sources, rewrite the previous implementation to modernize legacy API patterns to current Java standards.
Follow these rules exactly:
* Keep method and parameter names unchanged unless modernization requires it.
* Update deprecated API calls to modern equivalents.
* Apply current Java best practices and idioms.
* Maintain backward compatibility where possible.
* The function implementation should behave the same as the original implementation.
Write your modernized implementation of the `{function_name}`.
You must begin your response with ```{function_signature}```, and no extra text other than the code.
""".strip(),
                    "feedback_prompt": """
Given a previous implementation code and additional context sources, <candidate> is the rewritten previous implementation to modernize legacy API patterns.
Now your role is to check whether candidate satisfies these conditions:
* Properly updates deprecated API calls.
* Applies current Java best practices.
* Maintains backward compatibility where possible.
* The function implementation behaves the same as the original implementation.
For each point, specify <✅ or ❌> and give a short feedback.

Output only feedback. No Java code output.
""".strip(),
                    "correction_prompt": """
Given a previous implementation code and additional context sources, <candidate> is the rewritten previous implementation to modernize legacy API patterns.
Rewrite the previous implementation to properly modernize legacy API patterns to current Java standards.
Follow these rules exactly:
* Keep method and parameter names unchanged unless modernization requires it.
* Update deprecated API calls to modern equivalents.
* Apply current Java best practices and idioms.
* Maintain backward compatibility where possible.
* The function implementation should behave the same as the original implementation.
Write your modernized implementation of the `{function_name}`.
You must begin your response with ```{function_signature}```, and no extra text other than the code.
""".strip()
                },
                "incontext_config": {
                    "system_prompt": """You are an expert Java developer specializing in API modernization.

TASK: Modernize legacy API patterns to current Java standards.

INSTRUCTIONS:
1. Identify deprecated or outdated API usage patterns
2. Update to modern Java equivalents
3. Apply current Java best practices and idioms
4. Maintain backward compatibility where possible
5. Ensure the updated code follows modern conventions

CONVERSION PRINCIPLES:
- Update deprecated API calls to modern equivalents
- Apply modern Java features (Streams, Optional, etc.)
- Follow current naming and coding conventions
- Maintain original functionality and behavior
- Preserve error handling and edge cases
""",
                    "example_templates": {
                        "simple": """Example {number}:
Input:  {input_line}
Output: {output_line}
""",
                        "with_context": """Example {number}:
Context (before):
{context_before}
Input:  {input_line}
Output: {output_line}
Context (after):
{context_after}
""",
                        "with_explanation": """Example {number} (similarity: {similarity:.2f}):
Input:  {input_line}
Output: {output_line}
Explanation: {explanation}
"""
                    },
                    "instruction_templates": {
                        "basic": """MODERNIZE THE FOLLOWING:

{context_section}Input:  {query_line}
{context_after_section}Output: """,
                        "with_reasoning": """MODERNIZE THE FOLLOWING:

{context_section}Input:  {query_line}
{context_after_section}
Think step by step, then provide the modernized line.

Output: """,
                        "zero_shot": """MODERNIZE THE FOLLOWING:

No reference examples available. Apply general modernization principles.

{context_section}Input:  {query_line}
{context_after_section}Output: """
                    }
                },
                "domain_knowledge": {
                    "purpose": "Update outdated API patterns to modern Java practices"
                }
            }
        }
        
        return tasks.get(task_type, tasks["map_to_vo"])  # Default to map_to_vo

    @staticmethod
    def get_incontext_config(task_type: str) -> dict[str, Any]:
        """Get in-context learning specific configuration for a task"""
        task_config = TaskConfig.get_task_config(task_type)
        return task_config.get("incontext_config", {})

    @staticmethod
    def get_available_tasks() -> list[str]:
        """Get list of all available task types"""
        return ["map_to_vo", "legacy_api_modernization"]

    @staticmethod
    def get_task_description(task_type: str) -> str:
        """Get simple description for a task type"""
        descriptions = {
            "map_to_vo": "Convert data mapping operations to Value Object patterns.",
            "legacy_api_modernization": "Modernize legacy API patterns to current Java standards.",
            "default": "Transform the given code following the example patterns."
        }
        return descriptions.get(task_type, descriptions["default"])
