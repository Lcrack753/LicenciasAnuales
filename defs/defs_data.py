import sqlite3
from classes import license, agent
from defs_time import days_origin

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
                    admission TEXT,
                    year_2021 INTEGER,
                    year_2022 INTEGER,
                    year_2023 INTEGER,
                    year_2024 INTEGER,
                    year_2025 INTEGER,
                    year_2026 INTEGER
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

        # # TABLE days_left
        # cursor.execute("""CREATE TABLE days_available (
        #             id INTEGER PRIMARY KEY,
        #             cuil TEXT UNIQUE,
        #             year_2021 INTEGER,
        #             year_2022 INTEGER,
        #             year_2023 INTEGER,
        #             year_2024 INTEGER,
        #             year_2025 INTEGER,
        #             year_2026 INTEGER
        #             )""")

def connect_end(conn):
    conn.close()

# LISENSE
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


# AGENT
def update_days_origin(conn, cursor, cuil: str, admission):
    # Obtener los valores actuales de first y last
    cursor.execute("SELECT first, last FROM agent WHERE cuil = ?", (cuil,))
    result = cursor.fetchone()
    if result:
        first, last = result
        print(result)
    else:
        first, last = 'temp', 'temp'

    z = agent(cuil, first, last, admission).to_dict()

    with conn:
        cursor.execute("""UPDATE agent SET
                        admission = :admission,
                        year_2021 = :year_2021,
                        year_2022 = :year_2022,
                        year_2023 = :year_2023,
                        year_2024 = :year_2024,
                        year_2025 = :year_2025,
                        year_2026 = :year_2026 WHERE cuil = :cuil""",
                        z)

def push_agent(conn, cursor, obj: agent):
    with conn:
        cursor.execute("INSERT INTO agent (cuil, first, last, admission) VALUES (:cuil, :first, :last, :admission)", obj.to_dict())
        update_days_origin(conn,cursor,obj.cuil,obj.admission)

def fetch_agent(conn, cursor, query = None, select_days: bool = False):
    with conn:
        if select_days:
            columns = '*'
        else:
            columns = 'id, cuil, first, last, admission'
        if query is None:
            cursor.execute(f"SELECT {columns} FROM agent")
            return cursor.fetchall()
        try:
            query = int(query)
            cursor.execute(f"SELECT {columns} FROM agent WHERE cuil LIKE ?", ('%' + str(query) + '%',))
        except ValueError:
            cursor.execute(f"SELECT {columns} FROM agent WHERE first LIKE :query OR last LIKE :query", {'query': '%' + query + '%'})
        return cursor.fetchall()

# Creacion de la base de datos
if __name__ == "__main__":
    try:
        conn, cursor = connect_start('./data/dataBase.db')
        create_tables(conn,cursor)
        connect_end(conn)
    except sqlite3.OperationalError:
        print('database already exist')
