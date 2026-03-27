import sys
import os
sys.path.insert(0, os.path.abspath('d:/dexa/dexa'))

from dexa.orchestration.orchestrator import Orchestrator
import pandas as pd

df = pd.DataFrame({'A': [1, 2, None, 4, 5]})

orch = Orchestrator()
orch.set_data(df)

result = orch.run("give me average of column A")
print("\nFINAL RESULT:\n", result)

result2 = orch.run("fill NaN value in column A with average")
print("\nFINAL RESULT 2:\n", result2)
