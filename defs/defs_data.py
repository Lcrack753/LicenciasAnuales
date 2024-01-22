import sqlite3
import os
import csv
from .classes import License, Agent

# Connect to dataBase
def connect_start(database_path):
    conn = sqlite3.connect(database_path,check_same_thread=False)
    cursor = conn.cursor()
    return conn, cursor

# Creat tables
def create_tables(conn, cursor):
    with conn:
        # TABLE AGENT
        cursor.execute("""CREATE TABLE agent (
                    id INTEGER PRIMARY KEY,
                    cuil TEXT UNIQUE,
                    first TEXT,
                    last TEXT,
                    admission TEXT,
                    area TEXT
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

# End connection to database
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


def fetch_license(conn,cursor, cuil: str = None, date: str = None, reduce = False, fetch_headers: bool = False):
    with conn:
        if not cuil == None:
            cursor.execute("SELECT * FROM license WHERE cuil LIKE ?", ('%' + cuil + '%',))
        elif not date == None:
            cursor.execute("SELECT * FROM license WHERE start LIKE ?", ('%' + date + '%',))
        else:
            cursor.execute("SELECT * FROM license")
        
        rows = cursor.fetchall()
        if reduce:
            return [[row[2], row[4]] for row in rows]
        if fetch_headers:
            return [description[0] for description in cursor.description]
        return rows


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


# AGENT
def push_agent(conn, cursor, obj: Agent):
    with conn:
        cursor.execute("INSERT INTO agent (cuil, first, last, admission, area) VALUES (:cuil, :first, :last, :admission, :area)", obj.to_dict())


def fetch_agent(conn, cursor, query=None, fetch_headers=False):
    with conn:
        columns = 'id, cuil, first, last, admission, area'
        
        if query is None:
            cursor.execute(f"SELECT {columns} FROM agent")
            result = cursor.fetchall()
        else:
            cursor.execute(f"SELECT {columns} FROM agent WHERE cuil LIKE :query OR first LIKE :query OR last LIKE :query OR area LIKE :query", {'query': '%' + query + '%'})
            result = cursor.fetchall()

        if fetch_headers:
            return [description[0] for description in cursor.description]

        return result



def delete_agent(conn, cursor, obj: Agent):
    with conn:
        cursor.execute("""DELETE FROM agent WHERE
                            cuil = :cuil""",
                            obj.to_dict())


def tables_to_csv(conn, cursor):
    with conn:
        tables = ['agent','license']
        for table in tables:
            cursor.execute(f"SELECT * FROM {table}")
            data = cursor.fetchall()
            headers = [description[0] for description in cursor.description]
            make_csv(data,headers,f'{table}.csv')
            
def make_csv(table: list, headers: list = None, name: str = './result'):
    with open(name, 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)

        if not headers == None:
            print(len(headers), len(table[0]))
            if len(headers) != len(table[0]):
                raise ValueError('lenght_headers != lenght_table')
            escritor_csv.writerow(headers)

        # Escribir los datos
        escritor_csv.writerows(table)

def make_html(table: list, headers: list = None):    
    html = f""" <html>
                <table>
                    <tr>
                        {''.join([f'<th>{header}</th>' for header in headers])}
                    </tr>
                    {''.join([f'<tr>{"".join([f"<td>{cell}</td>" for cell in row])}</tr>' for row in table])}
                </table>
                </html>""".replace(" ", "").replace("\n", "")
    return html


# Creacion de la base de datos
if __name__ == "__main__":
    try:
        conn, cursor = connect_start('./data/dataBase.db')
        create_tables(conn,cursor)
        connect_end(conn)
    except ValueError:
        pass
