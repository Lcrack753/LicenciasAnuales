from classes import License, Agent
from defs_data import *


conn, cursor = connect_start('./data/dataBase.db')
maxi = Agent('20446415108','Maxi','Scri','01/01/2022','CSIS')
lic1 = License('20446415108','08/01/2024','14/01/2024')
lic2 = License('20446415108','20/02/2024','10/03/2024')

print(maxi.to_dict())
connect_end(conn)

