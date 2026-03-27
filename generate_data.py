import pandas as pd
import numpy as np

# Create a sample dataset with missing values and some patterns
df = pd.DataFrame({
    "age": [25, 30, np.nan, 40, 22, 35, np.nan, 28, 45, 32],
    "salary": [50000, 60000, 75000, np.nan, 45000, np.nan, 80000, 55000, 90000, 65000],
    "experience": [2, 5, 8, 10, 1, 7, 12, 3, 15, 6],
    "department": ["HR", "Eng", "Sales", "Eng", "HR", "Sales", "Eng", "HR", "Sales", "Eng"]
})

df.to_csv("test_data.csv", index=False)
print("Created test_data.csv with missing values.")
