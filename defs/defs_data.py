import sqlite3
from classes import license

def connect_start(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    return conn, cursor

def create_tables(conn, cursor):
    with conn:
        # TABLE AGENT
        cursor.execute("""CREATE TABLE agent (
                    id INTEGER PRIMARY KEY,
                    cuil TEXT UNIQUE,
                    first TEXT,
                    last TEXT,
                    admission TEXT
                    )""")

        # TABLE LICENSES
        cursor.execute("""CREATE TABLE license (
                    id INTEGER PRIMARY KEY,
                    cuil TEXT,
                    start TEXT,
                    end TEXT,
                    days_btw INTEGER,
                    note TEXT
                    )""")

        # TABLE days_left
        cursor.execute("""CREATE TABLE days_left (
                    id INTEGER PRIMARY KEY,
                    cuil TEXT UNIQUE,
                    year_2022 INTEGER,
                    year_2023 INTEGER,
                    year_2024 INTEGER,
                    year_2025 INTEGER,
                    year_2026 INTEGER
                    )""")

def connect_end(conn):
    conn.close()

# from classes import lisence
def push_lisense(conn, cursor, obj: license):
    with conn:
        cursor.execute("INSERT INTO license (cuil, start, end, days_btw, note) VALUES (:cuil, :start, :end, :days_btw, :note)", obj.to_dict())

def fetch_license(conn,cursor, cuil: str, date: str):
    with conn:
        if not cuil == None:
            cursor.execute("SELECT * FROM license WHERE cuil LIKE ?", ('%' + cuil + '%',))
        elif not date == None:
            cursor.execute("SELECT * FROM license WHERE start LIKE ?", ('%' + date + '%',))
        else:
            cursor.execute("SELECT * FROM license")
        
        rows = cursor.fetchall()
        return rows
    
    
# Creacion de la base de datos
if __name__ == "__main__":
    try:
        conn, cursor = connect_start('./data/dataBase.db')
        create_tables(conn,cursor)
        connect_end(conn)
    except sqlite3.OperationalError:
        print('database already exist')
    