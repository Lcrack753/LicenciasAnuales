import sqlite3

def connect_to_database(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    return conn, cursor

def create_tables(conn, cursor):
    with conn:
        # TABLE AGENT
        cursor.execute("""CREATE TABLE agent (
                    id INTEGER PRIMARY KEY,
                    cuil TEXT,
                    first TEXT,
                    last TEXT,
                    admission TEXT
                    )""")

        # TABLE LICENSES
        cursor.execute("""CREATE TABLE licenses (
                    id INTEGER PRIMARY KEY,
                    cuil TEXT,
                    start TEXT,
                    end TEXT,
                    note TEXT
                    )""")

        # TABLE days_left
        cursor.execute("""CREATE TABLE days_left (
                    id INTEGER PRIMARY KEY,
                    cuil TEXT,
                    year_2022 INTEGER,
                    year_2023 INTEGER,
                    year_2024 INTEGER,
                    year_2025 INTEGER,
                    year_2026 INTEGER
                    )""")

def close_connection(conn):
    conn.close()


