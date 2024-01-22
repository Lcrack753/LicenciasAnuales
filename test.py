from defs.classes import License, Agent
from defs.defs_data import *


conn, cursor = connect_start('./data/dataBase.db')


agent_instance = Agent(area='CSIS',last='CARNERO')
# push_agent(conn,cursor,agent_instance)

print(fetch_agent(conn,cursor))
# print(fetch_license(conn,cursor,reduce=True))