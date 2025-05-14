import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from typing import List, Tuple
from loguru import logger
from connect_database import MySQLConnect
from set_database import DatabaseInit
from csv_load import CSVLoad

class ImportData:
    def __init__(self, db, folder: str = "titanic_file", batch_size: int = 100):
        base_dir = os.path.dirname(__file__)
        self.load = CSVLoad(os.path.join(os.path.dirname(__file__), "titanic_file"))
        self.batch_size = batch_size
        self.db = db
        self.conn = db.conn
        self.cursor = db.cursor

    def connect(self):
        db = MySQLConnect()
        db.connect()
        self.conn = db.conn
        self.cursor = db.cursor

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn and self.conn.is_connected():
            self.conn.close()
            logger.success("")

    def import_all(self):
        csv_files = self.load.find_csv_files() #呼叫find_csv_files()  
        logger.info(f"CSV list：{csv_files}")
        #讀取load_csv()

        for file in tqdm(csv_files, desc="import CSV"):
            df = self.load.load_csv(file)
            table_name = os.path.splitext(os.path.basename(file))[0]
            insert_sql, clean_columns = self.clean_data(table_name, df)
            batch = []
            for _, row in df.iterrows():
                values = []
                for col in clean_columns:
                    value = row[col]
                    if pd.isna(value):
                        value = None
                    elif isinstance(value, (np.integer, np.floating)):
                        value = value.item()
                    values.append(value)
                batch.append(tuple(values))

                if len(batch) == self.batch_size:
                    self.cursor.executemany(insert_sql, batch)
                    self.conn.commit()
                    batch = []

                if batch:
                    self.cursor.executemany(insert_sql, batch)
                    self.conn.commit()
        self.close()

    def clean_data(self, table_name: str, df: pd.DataFrame) -> Tuple[str, List[str]]:
        df.columns = [str(col).strip().lower() for col in df.columns if pd.notna(col)]
        clean_columns = df.columns.tolist()

        placeholders = ", ".join(["%s"] * len(clean_columns))
        columns = ", ".join([f"`{col}`" for col in clean_columns])
        sql = f"INSERT IGNORE INTO `{table_name}` ({columns}) VALUES ({placeholders})"
        return sql, clean_columns


if __name__ == "__main__":
    db = MySQLConnect()
    db.connect()

    db_init = DatabaseInit(db)
    db_init.create_tables_from_csv()

    importer = ImportData(db=db)  # <<< 這裡加db=
    importer.import_all()
