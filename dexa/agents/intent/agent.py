from dexa.llm.abstraction import chat

class IntentAgent:
    def run(self, query: str, history: list = None, data_profile: dict = None):
        prompt = f"""
        Classify the user's intent.

        Query: {query}
        History: {history}
        Data Profile: {data_profile}

        Possible intents:
        - analyze
        - visualize
        - train_model
        - diagnose

        Also detect if this is a MACHINE LEARNING GOAL.

        Return:
        intent: <intent>
        goal: <yes/no>
        """

        return chat(prompt)