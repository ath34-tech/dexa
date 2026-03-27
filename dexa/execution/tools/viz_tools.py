from dexa.execution.tools.base import BaseTool
import matplotlib.pyplot as plt

class PlotHistogramTool(BaseTool):
    def __init__(self):
        super().__init__("plot_histogram", "Plots a histogram for a specified column.")

    def run(self, df=None, column=None, **kwargs):
        if df is not None and column in df.columns:
            plt.figure()
            df[column].hist()
            plt.title(f"Histogram of {column}")
            query_id = kwargs.get("query_id", "plot")
            filename = f"{query_id}.png"
            plt.savefig(filename)
            plt.close()
            summary = f"Histogram of {column} saved to {filename}"
            return {"summary": summary}
        return {"summary": f"Cannot plot. Column '{column}' not found."}
