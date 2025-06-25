import ollama
import json
import sys
from difflib import unified_diff
from agent_utils import Agent
from agent_utils import extract_methods, extract_method_bodies, matches_regardless_of_spacing
import re

def load_full_context(path):
    with open(path, 'r') as f:
        context = f.read()
    return context

full_context = load_full_context("sample/sample_input.txt")
java_code = load_full_context("/Users/heatz123/Documents/2025-1/InswaveWorkspace/test_examples/samples/file_sample_original/SampleTaskServiceImpl_in.java")
gt_java_code = load_full_context("/Users/heatz123/Documents/2025-1/InswaveWorkspace/test_examples/samples/file_sample_original/SampleTaskServiceImpl_in.java")
fn_names, fn_sigs = extract_methods(java_code)

# 2. Extract full function bodies from the ground-truth file
fn_bodies = extract_method_bodies(java_code, set(fn_names))
gt_fn_bodies = extract_method_bodies(gt_java_code, set(fn_names))

# 3. Example usage
for fn in fn_names:
    print(f"\nFunction: {fn}")
    print(gt_fn_bodies.get(fn, "[Not Found in GT]"))


# You are a Java code-conversion assistant.
BASIC_PROMPT = f"""
Given a previous implementation code, a reference Value Object class, and some additional previous context sources, rewrite the previous implementation to migrate from Map-based implementation to VO(Value Object)-based implementation, using the reference VO class provided whenever necessary.
Follow these rules exactly:
* Do NOT add, remove, or alter any comments.
* Keep method and parameter names unchanged.
* Keep all function and call names unchanged.
* Only change types (parameter, return, local) and the argument passed to calls.
* If the function implementation is using Map, convert it to use VO.
* The function implementation should behave the same as the original implementation.
Write your converted implementation of the `{fn_names[0]}` in the `Previous implementation (to convert to VO-based implementation)`.
You must begin your response with ```{fn_sigs[0]}```, and no extra text other than the code.
""".strip()
# Output only the Java code of the desired implementation to be converted (no extra text). 

if __name__ == "__main__":
    agent = Agent()

    # Check command-line flag
    use_diff = '--use-diff' in sys.argv
    use_feedback = '--use-feedback' in sys.argv

    prev_output = None
    feedback = None

    for i in range(1 if not use_feedback else 3):
        if prev_output is None:
            # first attempt
            prompt = f'''
{full_context}

{BASIC_PROMPT}
'''.strip()
            response = agent(prompt, clear_messages=True)
            GREEN = "\033[92m"   # prompt color
            CYAN  = "\033[96m"   # model response color
            RESET = "\033[0m"

            print("Prompt:\n", GREEN + prompt + RESET)
            print()
            print("Response:\n", CYAN + response + RESET)
            print()

            matches = re.findall(r"```(?:java)?\s*([\s\S]*?)\s*```", response)
            if matches:
                prev_output = matches[0]
            else:
                prev_output = response  # fallback if no match

            # evaluate the output
            if matches_regardless_of_spacing(prev_output, gt_fn_bodies[fn_names[0]]):
                print("Output matches ground truth! <check in emoji: ✅>")
            else:
                print("Output does not match ground truth! <check in emoji: ❌>")

        elif feedback is None:
            if use_diff:
                diff_text = '\n'.join(unified_diff(
                    fn_bodies.splitlines(),
                    prev_output.splitlines(),
                    fromfile='input',
                    tofile='candidate',
                    lineterm=''
                ))
            prompt = f"""
{full_context}

<candidate>
{prev_output}
</candidate>

{f'''<diff>
{diff_text}
</diff>
''' if use_diff else ''}

Given a previous implementation code, a reference Value Object class, and some additional previous context sources, <candidate> is the rewritten previous implementation to migrate from Map-based implementation to VO(Value Object)-based implementation, using the reference VO class provided.
Now your role is to check whether candidate satisfies these conditions:
* Do NOT add, remove, or alter any comments.
* Keep method and parameter names unchanged.
* Keep all function and call names unchanged.
* Only change types (parameter, return, local) and the argument passed to calls.
* If the function implementation is using Map, convert it to use VO.
* The function implementation should behave the same as the original implementation.
For each point, specify <✅ or ❌> and give a short feedback.

Output only feedback. No Java code output.
""".strip()
            response = agent(prompt, clear_messages=True)
            GREEN = "\033[92m"   # prompt color
            CYAN  = "\033[96m"   # model response color
            RESET = "\033[0m"

            print("Prompt:\n", GREEN + prompt + RESET)
            print()
            print("Response:\n", CYAN + response + RESET)
            print()

            feedback = response.strip("```java").strip("```")    

        else:
            prompt = f"""
{full_context}

<candidate>
{prev_output}
</candidate>

{f'''<diff>
{diff_text}
</diff>
''' if use_diff else ''}

<feedback>
{feedback}
</feedback>

Given a previous implementation code, a reference Value Object class, and some additional previous context sources, <candidate> is the rewritten previous implementation to migrate from Map-based implementation to VO(Value Object)-based implementation, using the reference VO class provided.
Rewrite the previous implementation to migrate from Map-based implementation to VO(Value Object)-based implementation, using the reference VO class provided whenever necessary.
Follow these rules exactly:
* Do NOT add, remove, or alter any comments.
* Keep method and parameter names unchanged.
* Keep all function and call names unchanged.
* Only change types (parameter, return, local) and the argument passed to calls.
* If the function implementation is using Map, convert it to use VO.
* The function implementation should behave the same as the original implementation.
Write your converted implementation of the `{fn_names[0]}` in the `Previous implementation (to convert to VO-based implementation)`.
You must begin your response with ```{fn_sigs[0]}```, and no extra text other than the code.
""".strip()

            response = agent(prompt, clear_messages=True)
            GREEN = "\033[92m"   # prompt color
            CYAN  = "\033[96m"   # model response color
            RESET = "\033[0m"

            print("Prompt:\n", GREEN + prompt + RESET)
            print()
            print("Response:\n", CYAN + response + RESET)
            print()

            matches = re.findall(r"```(?:java)?\s*([\s\S]*?)\s*```", response)
            if matches:
                prev_output = matches[0]
            else:
                prev_output = response  # fallback if no match

            feedback = None

    # Print final corrected method
    print("Final corrected method:")
    print(prev_output)

    # evaluate the output
    if matches_regardless_of_spacing(prev_output, gt_fn_bodies[fn_names[0]]):
        print("Output matches ground truth! <check in emoji: ✅>")
    else:
        print("Output does not match ground truth! <check in emoji: ❌>")