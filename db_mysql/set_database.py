import os
import pandas as pd
from typing import Dict
from loguru import logger
from connect_database import MySQLConnect
from csv_load import CSVLoad



class DatabaseInit:
    def __init__(self,db = None):
        self.db = MySQLConnect()
        self.csv_loader = CSVLoad(folder="titanic_file")


    def create_tables_from_csv(self):
        try:
            self.db.connect()
            csv_files = self.csv_loader.find_csv_files()

            for csv_file in csv_files:

                df = pd.read_csv(csv_file)
                table_name = os.path.splitext(os.path.basename(csv_file))[0]
                create_table_sql = self.create_sql_column(table_name, df)
                self.db.execute(create_table_sql)
                self.db.commit()

            logger.info("ALl table is success！")
        except Exception as e:
            logger.error(f"connect error and create error: {e}")
        finally:
            self.db.close()


    @staticmethod
    def create_sql_column(table_name: str, df: pd.DataFrame) -> str:
        type_mapping: Dict[str, str] = {
            "object": "VARCHAR(150)",
            "int64": "INT",
            "float64": "FLOAT",
            "bool": "BOOLEAN",
            "datetime64[ns]": "DATETIME"
        }

        columns = []
        primary_key = "passengerid"

        column_map = {col: col.strip().lower() for col in df.columns}

        for original_col, cleaned_col in column_map.items():
            dtype = df[original_col].dtype
            sql_type = type_mapping.get(str(dtype), "VARCHAR(150)")

            if cleaned_col == primary_key:
                columns.append(f"`{cleaned_col}` {sql_type} PRIMARY KEY")
            else:
                columns.append(f"`{cleaned_col}` {sql_type}")

        columns_sql = ",\n  ".join(columns)
        return f"""
        CREATE TABLE IF NOT EXISTS `{table_name}` (
          {columns_sql}
        );
        """


if __name__ == "__main__":
    db_init = DatabaseInit()
    db_init.create_tables_from_csv()
