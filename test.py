from defs.classes import License, Agent
from defs.defs_data import *


conn, cursor = connect_start('./data/dataBase.db')

agente = fetch_agent(conn,cursor,'20446415108')

obj = Agent(agente[0][1],admission=agente[0][4])


# push_lisense(conn,cursor,License('20','20/06/2025','30/06/2025'))
print(fetch_license(conn,cursor))
# print(fetch_license(conn,cursor,reduce=True))