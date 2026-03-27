import pandas as pd

class ProfilerAgent:
    def run(self, df: pd.DataFrame):
        return {
            "shape": df.shape,
            "columns": list(df.columns),
            "missing": df.isnull().sum().to_dict()
        }