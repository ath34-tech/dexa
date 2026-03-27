from dexa.execution.tools.base import BaseTool
import os
import pandas as pd

def _save_to_source(df):
    try:
        source_path_file = os.path.join(".dexa", "source_path.txt")
        if os.path.exists(source_path_file):
            with open(source_path_file, "r") as f:
                source_path = f.read().strip()
                
            if source_path and os.path.exists(source_path):
                if source_path.endswith('.csv'):
                    df.to_csv(source_path, index=False)
                elif source_path.endswith('.parquet'):
                    df.to_parquet(source_path)
                elif source_path.endswith(('.xls', '.xlsx')):
                    df.to_excel(source_path, index=False)
                return ""
            else:
                return f"\nWarning: Could not save to original file. The source path '{source_path}' does not exist."
        else:
            return "\nWarning: Could not save to original file! You must run 'dexa load-file <path>' to enable auto-saving for this session."
    except Exception as e:
        return f"\nFailed to explicitly save to source file: {e}"

class DescribeDataTool(BaseTool):
    def __init__(self):
        super().__init__("describe_data", "Provides descriptive statistics for the dataset.")

    def run(self, df=None, **kwargs):
        if df is not None:
            summary = df.describe().to_string()
            return {"summary": summary}
        return {"summary": "No data provided."}

class CheckMissingTool(BaseTool):
    def __init__(self):
        super().__init__("check_missing", "Checks for missing values in the dataset.")

    def run(self, df=None, **kwargs):
        if df is not None:
            summary = df.isnull().sum().to_string()
            return {"summary": summary}
        return {"summary": "No data provided."}

class DropMissingTool(BaseTool):
    def __init__(self):
        super().__init__("drop_missing", "Drops rows with missing values.")

    def run(self, df=None, **kwargs):
        if df is not None:
            old_shape = df.shape
            new_df = df.dropna()
            summary = f"Dropped rows with missing values. Shape changed from {old_shape} to {new_df.shape}."
            summary += _save_to_source(new_df)
            return {"summary": summary, "df": new_df}
        return {"summary": "No data provided."}

class FillMissingTool(BaseTool):
    def __init__(self):
        super().__init__("fill_missing", "Fills missing values with a specified strategy.")

    def run(self, df=None, column=None, strategy="mean", value=None, **kwargs):
        if df is not None and column in df.columns:
            new_df = df.copy()
            if value is not None:
                new_df[column] = new_df[column].fillna(value)
            elif strategy == "mean":
                new_df[column] = new_df[column].fillna(new_df[column].mean())
            elif strategy == "median":
                new_df[column] = new_df[column].fillna(new_df[column].median())
            elif strategy == "mode":
                new_df[column] = new_df[column].fillna(new_df[column].mode()[0])
            
            summary = f"Filled missing values in '{column}' using {strategy if value is None else f'constant {value}'}."
            summary += _save_to_source(new_df)
            return {"summary": summary, "df": new_df}
        return {"summary": f"Cannot fill missing. Column '{column}' not found or no data provided."}

class FilterDataTool(BaseTool):
    def __init__(self):
        super().__init__("filter_data", "Filters the dataset based on a boolean condition.")

    def run(self, df=None, condition=None, **kwargs):
        if df is not None and condition:
            try:
                new_df = df.query(condition)
                summary = f"Filtered data with condition: {condition}. New shape: {new_df.shape}."
                return {"summary": summary, "df": new_df}
            except Exception as e:
                return {"summary": f"Error filtering data: {str(e)}"}
        return {"summary": "No data provided or condition missing."}

class GetSampleTool(BaseTool):
    def __init__(self):
        super().__init__("get_sample", "Returns the first few rows of the dataset.")

    def run(self, df=None, n=5, **kwargs):
        if df is not None:
            summary = df.head(n).to_string()
            return {"summary": summary}
        return {"summary": "No data provided."}

class CreateColumnTool(BaseTool):
    def __init__(self):
        super().__init__("create_column", "Creates a new column with a specified value or evaluation expression.")

    def run(self, df=None, column=None, value=None, expression=None, **kwargs):
        if df is not None and column:
            new_df = df.copy()
            try:
                if expression:
                    new_df[column] = new_df.eval(expression)
                    summary = f"Created column '{column}' using expression '{expression}'."
                else:
                    new_df[column] = value
                    summary = f"Created column '{column}' filled with value '{value}'."
                summary += _save_to_source(new_df)
                return {"summary": summary, "df": new_df}
            except Exception as e:
                return {"summary": f"Error creating column: {str(e)}"}
        return {"summary": "No data provided or column name missing."}

class DropColumnTool(BaseTool):
    def __init__(self):
        super().__init__("drop_column", "Drops specified columns from the dataset.")

    def run(self, df=None, columns=None, **kwargs):
        if df is not None and columns:
            if isinstance(columns, str):
                columns = [columns]
            new_df = df.copy()
            existing_cols = [c for c in columns if c in new_df.columns]
            if existing_cols:
                new_df.drop(columns=existing_cols, inplace=True)
                summary = f"Dropped columns: {existing_cols}."
                summary += _save_to_source(new_df)
                return {"summary": summary, "df": new_df}
            else:
                return {"summary": f"None of the specified columns were found."}
        return {"summary": "No data provided or columns missing."}

class RenameColumnTool(BaseTool):
    def __init__(self):
        super().__init__("rename_column", "Renames columns based on a dictionary mapping.")

    def run(self, df=None, mapping=None, **kwargs):
        if df is not None and mapping and isinstance(mapping, dict):
            new_df = df.copy()
            new_df.rename(columns=mapping, inplace=True)
            summary = f"Renamed columns using mapping: {mapping}."
            summary += _save_to_source(new_df)
            return {"summary": summary, "df": new_df}
        return {"summary": "No data provided or invalid mapping dictionary."}

class SortDataTool(BaseTool):
    def __init__(self):
        super().__init__("sort_data", "Sorts the dataset by specified columns.")

    def run(self, df=None, columns=None, ascending=True, **kwargs):
        if df is not None and columns:
            if isinstance(columns, str):
                columns = [columns]
            try:
                new_df = df.sort_values(by=columns, ascending=ascending)
                summary = f"Sorted data by {columns} (ascending={ascending})."
                summary += _save_to_source(new_df)
                return {"summary": summary, "df": new_df}
            except Exception as e:
                return {"summary": f"Error sorting data: {str(e)}"}
        return {"summary": "No data provided or columns missing."}

class GroupByTool(BaseTool):
    def __init__(self):
        super().__init__("group_by", "Groups the dataset by columns and applies an aggregation.")

    def run(self, df=None, group_cols=None, agg_func="mean", **kwargs):
        if df is not None and group_cols:
            if isinstance(group_cols, str):
                group_cols = [group_cols]
            try:
                numeric_df = df.select_dtypes(include='number')
                grouped = df.groupby(group_cols)[numeric_df.columns] if not numeric_df.empty else df.groupby(group_cols)
                
                if agg_func == "mean":
                    new_df = grouped.mean().reset_index()
                elif agg_func == "sum":
                    new_df = grouped.sum().reset_index()
                elif agg_func == "count":
                    new_df = grouped.count().reset_index()
                elif agg_func == "max":
                    new_df = grouped.max().reset_index()
                elif agg_func == "min":
                    new_df = grouped.min().reset_index()
                else: return {"summary": f"Unsupported aggregation function: {agg_func}"}
                
                summary = f"Grouped by {group_cols} with aggregation '{agg_func}'. Result shape: {new_df.shape}."
                summary += _save_to_source(new_df)
                return {"summary": summary, "df": new_df}
            except Exception as e:
                return {"summary": f"Error grouping data: {str(e)}"}
        return {"summary": "No data provided or group columns missing."}

class ChangeDataTypeTool(BaseTool):
    def __init__(self):
        super().__init__("change_datatype", "Changes the data type of a column.")

    def run(self, df=None, column=None, target_type="str", **kwargs):
        if df is not None and column and column in df.columns:
            new_df = df.copy()
            try:
                if target_type in ['datetime', 'datetime64']:
                    new_df[column] = pd.to_datetime(new_df[column], errors='coerce')
                elif target_type in ['numeric']:
                    new_df[column] = pd.to_numeric(new_df[column], errors='coerce')
                else:
                    new_df[column] = new_df[column].astype(target_type)
                
                summary = f"Changed data type of '{column}' to '{target_type}'."
                summary += _save_to_source(new_df)
                return {"summary": summary, "df": new_df}
            except Exception as e:
                return {"summary": f"Error converting data type: {str(e)}"}
        return {"summary": "No data provided or column missing."}
