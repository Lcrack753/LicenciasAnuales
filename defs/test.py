from classes import license
from defs_data import *

lucio = license('20448919936', '05/02/2023', '25/02/2023', '-')

conn, cursor = connect_start('./data/dataBase.db')
push_lisense(conn, cursor, lucio)
push_lisense(conn, cursor, lucio)
push_lisense(conn, cursor, lucio)
push_lisense(conn, cursor, lucio)
push_lisense(conn, cursor, lucio)

for row in fetch_license(conn, cursor,cuil=None,date='2023'):
    print(row)