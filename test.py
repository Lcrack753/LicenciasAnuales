from defs.classes import License, Agent
from defs.defs_data import *


conn, cursor = connect_start('./data/dataBase.db')

agente = fetch_agent(conn,cursor,'20446415108')

obj = Agent(agente[0][1],admission=agente[0][4])

print(agente)
print(obj.to_dict())
print(obj.days_available(to_dict=True))
# print(fetch_license(conn,cursor,reduce=True))