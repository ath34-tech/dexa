from dexa.llm.abstraction import chat

class ResponseAgent:
    def run(self, query: str, reasoning: str, data_profile: dict = None):
        prompt = f"""
        Format the final reasoning into a natural language response for the user.
        
        User's Current Query: {query}
        Execution History Context: {reasoning}
        Dataset Overview / Profile: {data_profile}
        
        CRITICAL INSTRUCTION:
        1. Answer the User's Current Query directly based on the most recent relevant information in the Execution History Context. Do not summarize old or unrelated tasks from the history.
        2. DO NOT show JSON tool payloads to the user. For simple queries using predefined tools, just give them the direct answers without breaking down the JSON.
        3. For complex queries where the Execution History shows custom Python code was explicitly generated and executed, you MUST briefly show the user the exact Python code snippet that was run in a markdown block, followed immediately by its execution results.
        4. If the user asks a simple question (e.g., "what is the average?", "give me the count", "correlation of features"), just give them the actual value directly without adding "actionable ML insights" or verbose bullet points. Only add extra insights if asked for analysis.
        """
        return chat(prompt)