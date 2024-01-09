import sqlite3
from classes import license, agent
from defs_time import f_check

def connect_start(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    return conn, cursor

def create_tables(conn, cursor,year: int):
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

def connect_end(conn):
    conn.close()

# LISENSE
def push_lisense(conn, cursor, obj: license):
    with conn:
        cursor.execute("SELECT * FROM agent WHERE cuil = ?", (obj.cuil,))
        if cursor.fetchone() is None:
            raise ValueError('cuil doesnt exist in agent table')
        
        cursor.execute("""SELECT * FROM license WHERE
                        cuil = :cuil AND
                        (start = :start OR
                        end = :end)""",
                        obj.to_dict())
        if cursor.fetchone():
            raise ValueError('repited value in license')
        
        cursor.execute("INSERT INTO license (cuil, start, end, days_btw, note) VALUES (:cuil, :start, :end, :days_btw, :note)", obj.to_dict())

def fetch_license(conn,cursor, cuil: str = None, date: str = None):
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
        cursor.execute(f"SELECT {columns} FROM agent WHERE cuil LIKE :query OR first LIKE :query OR last LIKE :query", {'query': '%' + query + '%'})
        return cursor.fetchall()

# delete
def delete_license(conn,cursor,obj: license, all_instance_of_cuil: bool = False):
    with conn:
        if all_instance_of_cuil == True:
            cursor.execute("""DELETE FROM license WHERE
                        cuil = :cuil""",
                        obj.to_dict())
        else:
            cursor.execute("""DELETE FROM license WHERE
                        cuil = :cuil AND
                        start = :start AND
                        end = :end""",
                        obj.to_dict())

def calculate_days_avalible(conn,cursor, cuil: str):
    with conn:
        cursor.execute("""SELECT start FROM license WHERE cuil = ?""", (cuil,))
        rows = cursor.fetchall()
        dates_order = []
        for row in rows:
            dates_order.append(row[0])
        

# Creacion de la base de datos
if __name__ == "__main__":
    try:
        conn, cursor = connect_start('./data/dataBase.db')
        create_tables(conn,cursor)
        connect_end(conn)
    except sqlite3.OperationalError:
        print('database already exist')
