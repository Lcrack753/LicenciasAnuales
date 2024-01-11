from classes import License, Agent
from defs_data import *


conn, cursor = connect_start('./data/dataBase.db')
cursor.description
mutu = Agent('123', 'lucio', 'capo', '01/08/2023', 'cis')
mutu_lic = License('123','19/02/2024','07/03/2024','-')

#push_lisense(conn,cursor,mutu_lic)
headers = fetch_license(conn,cursor,fetch_headers=True)
data = fetch_license(conn,cursor)

print(data)
print(make_html(data, headers))
connect_end(conn)

