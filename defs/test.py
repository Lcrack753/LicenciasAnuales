from classes import License, Agent
from defs_data import *


conn, cursor = connect_start('./data/dataBase.db')

mutu = Agent('1516514651', 'mutu', 'gay', '01/02/2023', 'cis')
mutu_lic = License('1516514651','19/02/2024','07/03/2024','-')

print(mutu.days_origin_dict)
print(mutu_lic.days_btw)
#make_csv(conn,cursor)
connect_end(conn)

