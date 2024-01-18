from defs.classes import License, Agent
from defs.defs_data import *


conn, cursor = connect_start('./data/dataBase.db')

print(fetch_agent(conn, cursor))

