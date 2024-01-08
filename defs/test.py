from classes import license, agent
from defs_data import *

lucio = agent('123456789','Ciro','Heianna','05/01/2022')

lic1 = license('123456789', '15/01/2024', '21/01/2024', '-')

conn, cursor = connect_start('./data/dataBase.db')

# push_agent(conn,cursor,lucio)
# push_lisense(conn,cursor, lic1)
# update_days_origin(conn,cursor,'','2024-08-02')

delete_license(conn,cursor,lic1)
print(fetch_license(conn,cursor))
# print(fetch_agent(conn,cursor,select_days=False,query='4'))
connect_end(conn)

