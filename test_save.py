import pandas as pd
import os
from dexa.orchestration.orchestrator import Orchestrator
from dexa.execution.tools.registry import TOOLS

# Create dummy csv
df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
df.to_csv("dummy.csv", index=False)

# Load via orchestrator
orch = Orchestrator()
orch.load_file("dummy.csv")

# Verify source_path
source_path_file = ".dexa/source_path.txt"
with open(source_path_file, "r") as f:
    print("Source path written:", f.read().strip())

# Execute CreateColumnTool
create_col_tool = TOOLS["create_column"]
res = create_col_tool.run(df=pd.read_csv("dummy.csv"), column="C", value=5)

# Verify if dummy.csv was modified
df_modified = pd.read_csv("dummy.csv")
print("Columns in dummy.csv after tool execution:", df_modified.columns.tolist())
