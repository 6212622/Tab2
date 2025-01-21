import pyodbc

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=192.168.104.10;"
    "DATABASE=tabel;"
    "UID=1c-user;"
    "PWD=M()nsterK!11;"
)

try:
    conn = pyodbc.connect(connection_string)
    print("Подключение к SQL Server успешно!")
    conn.close()
except Exception as e:
    print(f"Ошибка подключения: {e}")
