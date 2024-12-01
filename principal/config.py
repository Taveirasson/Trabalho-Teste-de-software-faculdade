import pyodbc
from contextlib import contextmanager

@contextmanager
def conectar_banco(driver = "ODBC Driver 17 for SQL Server", server="localhost", database="DB_Loja", trusted_connection="yes"):
    connection_string = (
        f"Driver={{{driver}}};"
        f"Server={server};"  
        f"Database={database};"  
        f"Trusted_Connection={trusted_connection};" 
    )
    conn = pyodbc.connect(connection_string)
    try:
        yield conn
    finally:
        conn.close()