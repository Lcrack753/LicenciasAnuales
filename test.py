from defs.classes import License, Agent
from defs.defs_data import *


conn, cursor = connect_start('./data/dataBase.db')
Lucio = Agent()
lic1 = License('20446415108','08/01/2024','14/01/2024')
lic2 = License('20446415108','20/02/2024','10/03/2024')

push_agent(conn,cursor,Lucio)
print(fetch_agent(conn, cursor))

