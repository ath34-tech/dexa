import pandas as pd
import os

# Persistence path
STORAGE_DIR = ".dexa"
STORAGE_FILE = os.path.join(STORAGE_DIR, "current_data.parquet")

# Default sample data
DEFAULT_DF = pd.DataFrame({
    "age": [22, 25, 30, 35, 40],
    "salary": [20000, 25000, 40000, 50000, 60000],
    "experience": [1, 2, 5, 7, 10]
})

_active_df = None

def get_data():
    global _active_df
    if _active_df is not None:
        return _active_df
    
    # Try loading from disk
    if os.path.exists(STORAGE_FILE):
        try:
            _active_df = pd.read_parquet(STORAGE_FILE)
            return _active_df
        except:
            pass
            
    # Fallback to default
    _active_df = DEFAULT_DF
    return _active_df

def set_data(df: pd.DataFrame):
    global _active_df
    _active_df = df
    
    # Save to disk for cross-command persistence
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)
    
    try:
        df.to_parquet(STORAGE_FILE)
    except Exception as e:
        print(f"Warning: Failed to persist data to disk: {e}")
        
    # Attempt to sync changes back to original file if present
    try:
        source_path_file = os.path.join(STORAGE_DIR, "source_path.txt")
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
    except Exception as e:
        print(f"Warning: Failed to sync data to original source ({source_path}): {e}")
