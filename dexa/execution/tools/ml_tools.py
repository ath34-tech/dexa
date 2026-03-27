from dexa.execution.tools.base import BaseTool
from sklearn.linear_model import LinearRegression

class TrainLinearModelTool(BaseTool):
    def __init__(self):
        super().__init__("train_linear_model", "Trains a simple linear regression model.")

    def run(self, df=None, target_col=None, **kwargs):
        if df is not None and target_col in df.columns:
            try:
                X = df.drop(columns=[target_col])
                y = df[target_col]
                model = LinearRegression()
                model.fit(X, y)
                summary = f"Model trained successfully. Coefficients: {model.coef_}, Intercept: {model.intercept_}"
                return {"summary": summary}
            except Exception as e:
                return {"summary": f"Error training model: {str(e)}"}
        return {"summary": f"Cannot train model. Data or target column '{target_col}' missing."}
