import sqlite3
import os
import csv
from classes import License, Agent

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
                    area TEXT,
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
def push_lisense(conn, cursor, obj: License):
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

def fetch_license(conn,cursor, cuil: str = None, date: str = None, reduce = False):
    with conn:
        if not cuil == None:
            cursor.execute("SELECT * FROM license WHERE cuil LIKE ?", ('%' + cuil + '%',))
        elif not date == None:
            cursor.execute("SELECT * FROM license WHERE start LIKE ?", ('%' + date + '%',))
        else:
            cursor.execute("SELECT * FROM license")
        
        rows = cursor.fetchall()
        if reduce == True:
            return [[row[2], row[4]] for row in rows]
        return rows


def push_agent(conn, cursor, obj: Agent):
    with conn:
        cursor.execute("INSERT INTO agent (cuil, first, last, admission) VALUES (:cuil, :first, :last, :admission, :area)", obj.to_dict())


def fetch_agent(conn, cursor, query = None):
    with conn:
        columns = 'id, cuil, first, last, admission'
        if query is None:
            cursor.execute(f"SELECT {columns} FROM agent")
            return cursor.fetchall()
        cursor.execute(f"SELECT {columns} FROM agent WHERE cuil LIKE :query OR first LIKE :query OR last LIKE :query OR area LIKE :query", {'query': '%' + query + '%'})
        return cursor.fetchall()


# delete
def delete_license(conn,cursor,obj: License, all_instance_of_cuil: bool = False):
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


def tables_to_csv(conn, cursor):
    with conn:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            make_csv(table[0], name=f'database_{table[0]}')
            csv.DictWriter()
            
def make_csv(table: list, description, name: str):
    with open(f'{name}.csv', 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)

        # Escribir los encabezados de columna
        encabezados = [descripcion[0] for descripcion in description]
        escritor_csv.writerow(encabezados)

        # Escribir los datos
        escritor_csv.writerows(table)

# Creacion de la base de datos
if __name__ == "__main__":
    try:
        conn, cursor = connect_start('./data/dataBase.db')
        create_tables(conn,cursor)
        connect_end(conn)
    except sqlite3.OperationalError:
        print('database already exist')
