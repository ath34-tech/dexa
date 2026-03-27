from dexa.llm.abstraction import chat

class GoalAgent:
    def run(self, query: str):
        prompt = f"""
        You are a senior ML engineer.

        User goal:
        {query}

        Identify:
        - Problem type (classification/regression/clustering)
        - Target variable
        - Suggested features
        - Suggested models
        - Evaluation metric

        Keep it structured.
        """

        return chat(prompt)