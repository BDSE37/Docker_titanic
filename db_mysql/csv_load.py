import os
import pandas as pd
from typing import List, Tuple

class CSVLoad:

    def __init__(self, folder: str = "titanic_file"):
        self.folder = os.path.join(os.getcwd(), folder)

    def find_csv_files(self) -> List[str]:
        csv_files = []
        for root, _, files in os.walk(self.folder):
            for file in files:
                if file.lower().endswith(".csv") and not file.startswith("."):
                    full_path = os.path.join(root, file)
                    csv_files.append(full_path)
        return csv_files


    def load_csv(self, filepath: str) -> pd.DataFrame:
        df = pd.read_csv(filepath)
        df.columns = [col.strip() for col in df.columns if pd.notna(col)]
       
        return df

    def load_all_csv(self) -> List[Tuple[str, pd.DataFrame]]:
        all_data = []
        for filepath in self.find_csv_files():
            table_name = os.path.splitext(os.path.basename(filepath))[0]
            df = self.load_csv(filepath)
            all_data.append((table_name, df))
        return all_data
