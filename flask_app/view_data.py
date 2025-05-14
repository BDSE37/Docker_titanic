import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'db_mysql')))
from loguru import logger
from connect_database import MySQLConnect

class ViewData:
    def __init__(self):
        self.db = MySQLConnect()
        self.db.connect()

    def fetch_passenger_chunk(self, offset: int, limit: int, search: str = "", order_column: str = "PassengerId", order_dir: str = "asc"):
        cursor = self.db.conn.cursor(dictionary=True)

        allowed_columns = {
            "PassengerId", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked", "Survived"
        }
        if order_column not in allowed_columns:
            order_column = "PassengerId"
        if order_dir.lower() not in ("asc", "desc"):
            order_dir = "asc"

        like_query = f"%{search}%"

        if search:
            query = f"""
                SELECT PassengerId, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked, Survived
                FROM train
                WHERE LOWER(Name) LIKE LOWER(%s)
                   OR LOWER(Ticket) LIKE LOWER(%s)
                   OR LOWER(Cabin) LIKE LOWER(%s)
                   OR LOWER(Sex) LIKE LOWER(%s)
                ORDER BY {order_column} {order_dir}
                LIMIT %s OFFSET %s
            """
            cursor.execute(query, (like_query, like_query, like_query, like_query, limit, offset))
        else:
            query = f"""
                SELECT PassengerId, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked, Survived
                FROM train
                ORDER BY {order_column} {order_dir}
                LIMIT %s OFFSET %s
            """
            cursor.execute(query, (limit, offset))

        rows = cursor.fetchall()
        cursor.close()
        return rows

    def get_passenger_count(self, search: str = "") -> int:
        cursor = self.db.conn.cursor()
        like_query = f"%{search}%"

        if search:
            query = """
                SELECT COUNT(*) FROM train
                WHERE LOWER(Name) LIKE LOWER(%s)
                   OR LOWER(Ticket) LIKE LOWER(%s)
                   OR LOWER(Cabin) LIKE LOWER(%s)
                   OR LOWER(Sex) LIKE LOWER(%s)
            """
            cursor.execute(query, (like_query, like_query, like_query, like_query))
        else:
            cursor.execute("SELECT COUNT(*) FROM train")

        count = cursor.fetchone()[0]
        cursor.close()
        return count
