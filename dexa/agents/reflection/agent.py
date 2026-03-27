from dexa.llm.abstraction import chat

class ReflectionAgent:
    def run(self, result: str):
        prompt = f"""
        Evaluate the result of the last execution.
        Result: {result}

        OUTPUT FORMAT:
        {{
            "decision": "continue | replan | stop",
            "reason": "...",
            "issues": [],
            "confidence": 0-1
        }}

        Return ONLY valid JSON.
        """
        return chat(prompt)