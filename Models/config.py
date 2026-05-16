import pyodbc

class Database:
    def __init__(self):
        self.conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=Rooker\\SQLEXPRESS;'
            'DATABASE=NSVQA_APP;'
            'Trusted_Connection=yes;'
        )

    def execute(self, query, params=()):
        cursor = self.conn.cursor()      # new cursor each time
        cursor.execute(query, params)
        return cursor                    # still returns cursor (like before)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()