
from dexa.llm.abstraction import chat

class VisualizationAgent:
    def run(self, history: list, dataset_info: str):
        prompt = f"""
        You are a visualization expert.
        Based on the history of execution and dataset information, decide if a visualization is needed.

        History:
        {history}

        Dataset Info:
        {dataset_info}

        Output Format:
        {{
            "should_visualize": true/false,
            "plot_type": "histogram",
            "column": "..."
        }}

        Return ONLY valid JSON.
        """
        return chat(prompt)