from dexa.graph.graph_builder import build_graph
import pandas as pd
import os
from dexa.execution.data_store import get_data, set_data

class Orchestrator:
    
    def __init__(self, session_id="default"):
        self.graph = build_graph()
        self.session_id = session_id
    
    @classmethod
    def set_data(cls, df: pd.DataFrame):
        set_data(df)

    def load_file(self, file_path: str):
        if not os.path.exists(file_path):
            return f"Error: File {file_path} not found."
        
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.parquet'):
                df = pd.read_parquet(file_path)
            elif file_path.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file_path)
            else:
                return "Error: Unsupported file format. Use CSV, Parquet, or Excel."
            
            # Save the original absolute path
            from dexa.execution.data_store import STORAGE_DIR
            if not os.path.exists(STORAGE_DIR):
                os.makedirs(STORAGE_DIR)
            with open(os.path.join(STORAGE_DIR, "source_path.txt"), "w") as f:
                f.write(os.path.abspath(file_path))

            set_data(df)
            return f"Successfully loaded data from {file_path}. Shape: {df.shape}"
        except Exception as e:
            return f"Error loading file: {str(e)}"

    def load_kaggle(self, dataset_identifier: str):
        # identifier is 'username/dataset-name'
        try:
            from dexa.cli.main import DOTENV_PATH
            from dotenv import load_dotenv
            load_dotenv(DOTENV_PATH)
            
            username = os.getenv("KAGGLE_USERNAME")
            key = os.getenv("KAGGLE_KEY")

            if not username or not key:
                return "Error: Kaggle credentials not found. Use 'config --kaggle-username ... --kaggle-key ...' to set them."

            # Ensure they are in os.environ for the kaggle library
            os.environ["KAGGLE_USERNAME"] = username
            os.environ["KAGGLE_KEY"] = key
            os.environ["KAGGLE_API_TOKEN"] = key # Some tokens might use this

            from kaggle.api.kaggle_api_extended import KaggleApi
            api = KaggleApi()
            api.authenticate()
            
            temp_dir = "kaggle_data"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            
            # Download dataset
            api.dataset_download_files(dataset_identifier, path=temp_dir, unzip=True)
            
            # Find the first CSV/Parquet file in the downloaded files
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith(('.csv', '.parquet')):
                        file_path = os.path.join(root, file)
                        return self.load_file(file_path)
            
            return "Error: No CSV or Parquet file found in the Kaggle dataset."
        except Exception as e:
            return f"Error loading Kaggle dataset: {str(e)}"

    def run(self, query: str):
        # Initialize config for persistence
        config = {"configurable": {"thread_id": self.session_id}}
        
        # Initialize state
        initial_state = {
            "query": query,
        }
        
        # Invoke graph with config
        final_state = self.graph.invoke(initial_state, config=config)
        
        return final_state.get("final_response", "No response generated.")