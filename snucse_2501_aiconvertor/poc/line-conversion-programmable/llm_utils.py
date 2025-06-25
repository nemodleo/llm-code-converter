import ollama

class Agent:
    def __init__(self, model='llama3.2', system_prompt=None):
        self.model = model
        self.messages = []
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    def __call__(self, user_prompt: str, clear_messages=True):

        if clear_messages:
            self.messages = self.messages[1:]
        self.messages.append({"role": "user", "content": user_prompt})

        response = ollama.chat(
            model=self.model,
            messages=self.messages,
            options={"temperature": 0.0}
        )
        reply = response['message']['content']
        self.messages.append({"role": "assistant", "content": reply})

        return reply
    