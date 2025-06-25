import ollama


class Agent:
    def __init__(
            self,
            model='qwen2.5-coder:7b',
            temperature=0.0,
            system_prompt=None,
            verbose=False
    ):

        self.model = model
        self.temperature = temperature
        self.verbose = verbose
        self.messages = []
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    def __call__(self, user_prompt: str, clear_messages=True, max_lines=None):
        if clear_messages:
            self.messages = self.messages[1:]

        self.messages.append({"role": "user", "content": user_prompt})

        options = {"temperature": self.temperature}

        if self.verbose and max_lines is not None:
            print(f"[Max lines limit: {max_lines}]")
        if self.verbose:
            print("[Assistant]: ", end='', flush=True)

        # stream=True로 실시간 처리하여 라인 수 제한
        stream = ollama.chat(
            model=self.model,
            messages=self.messages,
            options=options,
            stream=True
        )

        reply_parts = []
        line_count = 0

        for chunk in stream:
            content = chunk['message']['content']

            # max_lines 제한이 있는 경우 라인 수 체크
            if max_lines is not None:
                # 현재까지의 내용에 새 content를 추가했을 때의 라인 수 계산
                temp_content = ''.join(reply_parts) + content
                new_line_count = temp_content.count('\n')

                # 라인 수 제한 초과 시 중단
                if new_line_count >= max_lines:
                    # 제한 라인까지만 포함하도록 content 자르기
                    remaining_lines = max_lines - line_count
                    if remaining_lines > 0:
                        lines_in_content = content.split('\n')
                        if len(lines_in_content) > remaining_lines:
                            content = '\n'.join(lines_in_content[:remaining_lines])
                        reply_parts.append(content)
                        line_count = max_lines
                    break
                
                line_count = new_line_count
            
            reply_parts.append(content)
            if self.verbose:
                print(content, end='', flush=True)

        reply = ''.join(reply_parts)

        if self.verbose:
            if max_lines is not None and line_count >= max_lines:
                print(f" [Stopped at {max_lines} lines]")
            print()

        self.messages.append({"role": "assistant", "content": reply})
        return reply
