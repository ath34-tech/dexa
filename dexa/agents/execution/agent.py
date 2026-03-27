from dexa.llm.abstraction import chat

class ExecutionAgent:
    def run(self, query: str, plan: str, history: list = None, data_profile: dict = None):
        prompt = f"""
        You are an expert data science agent.

        User Query:
        {query}

        Current Step in Plan:
        {plan}

        Execution History:
        {history}

        Data Profile (Column names, types, etc.):
        {data_profile}

        YOUR TASK:
        Execute ONLY the "Current Step in Plan". 
        Do NOT execute the entire plan at once.
        Do NOT provide multiple tool calls.

        Decide whether to use a pre-defined tool or generate Python code.
        Prefer tools where possible.

        AVAILABLE TOOLS:
        - describe_data: Provides descriptive statistics.
        - check_missing: Checks for missing values.
        - drop_missing: Drops rows with missing values.
        - fill_missing(column, strategy='mean'|'median'|'mode'|None, value=None): Fills missing values.
        - filter_data(condition): Filters data based on a query string (e.g., 'age > 30').
        - get_sample(n=5): Returns first n rows.
        - create_column(column, value=None, expression=None): Creates a column with a constant value or a string eval expression (e.g. 'A + B').
        - drop_column(columns): Drops one or a list of columns.
        - rename_column(mapping): Renames columns using a dict mapping (e.g., {{'old': 'new'}}).
        - sort_data(columns, ascending=True): Sorts data by columns.
        - group_by(group_cols, agg_func='mean'|'sum'|'count'|'max'|'min'): Groups and aggregates numeric columns.
        - change_datatype(column, target_type='int'|'float'|'str'|'datetime'): Casts a column to a new type.
        - train_linear_model(target_col): Trains linear regression.
        - plot_histogram(column): Plots a histogram.

        PREFER TOOLS OVER CUSTOM CODE.
        If a task can be done with a tool, use it. Only use "code" for complex operations not covered by tools.

        IMPORTANT: If you use the "code" option:
        1. You have access to exactly three variables: `df` (the pandas DataFrame), `data_profile` (the metadata dictionary), and `query_id` (a unique request hash).
        2. You MUST use `print(...)` to output any information, calculations, or results. Only standard output is captured!
        3. If you generate any visualizations/plots, you MUST save the file using the injected `query_id` variable (e.g. `plt.savefig(f'{{query_id}}.png')`). DO NOT use `plot.png` or `plt.show()`.

        EITHER:
        {{
            "type": "tool",
            "tool_name": "...",
            "args": {{}}
        }}
        OR:
        {{
            "type": "code",
            "code": "print(df['column'].mean())"
        }}

        Return ONLY valid JSON. Do NOT wrap it in ```json or ```markdown. Just output the raw JSON object. Make sure the JSON is perfectly formatted.
        """

        return chat(prompt)