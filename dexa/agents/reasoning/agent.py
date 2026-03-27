from dexa.llm.abstraction import chat

class ReasoningAgent:
    def run(self, result: list):
        prompt = f"""
        Synthesize insights from the execution history.
        History: {result}

        Provide actionable ML insights, not generic summaries.Only provide answer for stuff that you have been asked.
        """
        return chat(prompt)