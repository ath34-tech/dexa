from dexa.llm.abstraction import chat

class PlannerAgent:
    def run(self, intent: str, query: str, history: list = None, data_profile: dict = None):
        prompt = f"""
        Create a concise plan for the query.
        Query: {query}
        Intent: {intent}
        History: {history}
        Data Profile: {data_profile}

        Max 3-5 steps.
        Avoid overplanning.
        Each step must be a single, executable action.

        Return steps as a newline separated list.
        Do NOT add numbering or extra text.
        """
        return chat(prompt)