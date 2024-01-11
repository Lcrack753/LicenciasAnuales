from classes import License, Agent
from defs_data import *


conn, cursor = connect_start('./data/dataBase.db')
mutu = Agent()
mutu_lic = License('123','02/05/2025','07/04/2025','-')
print(mutu.to_dict())
print(mutu.days_available())
connect_end(conn)

