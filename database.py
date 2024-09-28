from contextlib import contextmanager
import os
import pyodbc

class DataBase:
    def __init__(self):
        MODE = os.environ.get('MODE', 'development')
        if MODE == 'production':
            self.connection_string = (
                'Driver={ODBC Driver 18 for SQL Server};'
                f'Server=tcp:{os.environ["AZURE_SQL_SERVER"]},{os.environ["AZURE_SQL_PORT"]};'
                f'Database={os.environ["AZURE_SQL_DATABASE"]};'
                f'UID={os.environ["AZURE_SQL_USER"]};'
                f'PWD={os.environ["AZURE_SQL_PASSWORD"]};'
                'Encrypt=yes;'
                'TrustServerCertificate=no;'
                'Connection Timeout=30'
            )
        else:
            self.connection_string = (
                'Driver={ODBC Driver 18 for SQL Server};'
                'Server=localhost;'
                'Database=AzTest;'
                'Encrypt=yes;'
                'TrustServerCertificate=yes;'
                'Trusted_Connection=yes;'
            )

    @contextmanager
    def connect(self):
        connection = pyodbc.connect(self.connection_string)
        try:
            yield connection
        except Exception as e:
            connection.rollback()
            raise e
        else:
            connection.commit()
        finally:
            connection.close()
