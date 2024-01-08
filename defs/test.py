from classes import license, agent
from defs_data import *

lucio = agent('204485984','Roberto','Carnero','01/08/2023')

conn, cursor = connect_start('./data/dataBase.db')

# push_agent(conn,cursor,lucio)
update_days_origin(conn,cursor,'','2024-08-02')
print(fetch_agent(conn,cursor,select_days=True))
connect_end(conn)

