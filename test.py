from defs.classes import License, Agent
from defs.defs_data import *


conn, cursor = connect_start('./data/dataBase.db')


agent_instance = Agent(area='CSIS',last='CARNERO')
# push_agent(conn,cursor,agent_instance)
push_lisense(conn,cursor,License('3','15/6/2022','20/6/2022'))
print(fetch_agent(conn,cursor))
print(fetch_license(conn,cursor))
# print(fetch_license(conn,cursor,reduce=True))