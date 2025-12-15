class Agent:
    def __init__(self, name, system_prompt, engine):
        self.name = name
        self.system_prompt = system_prompt
        self.engine = engine
        self.history = []

    def think(self, user_input):
        print(f"\n⚡ {self.name} is thinking...")

        # Construct message history
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.history)
        messages.append({"role": "user", "content": user_input})

        # Call the Engine
        response = self.engine.generate(messages)

        # Save to memory
        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": response})

        return response
