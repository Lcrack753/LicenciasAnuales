from classes import License, Agent
from defs_data import *

lucio = Agent('20448919936','Lucio', 'Carnero','01/08/2021')
""" lic1 = License('20448919936','2021-06-26','2021-07-15','-')
lic2 = License('20448919936','2023-08-06','2023-08-15','-')
lic3 = License('20448919936','2025-01-07','2025-01-20','-') """



""" conn, cursor = connect_start('./data/dataBase.db')
days_lucio = days_available(fetch_license(conn,cursor,'2044',reduce=True),lucio.days_origin_to_tuple())

# print(lucio.days_origin_to_tuple())
print(fetch_license(conn,cursor,'2044',reduce=True))
print(days_lucio.agent_days)
print(days_lucio.to_dict()) """

origin = lucio.days_available([['2021-12-26', 6], ['2023-06-26', 14], ['2023-12-26', 6], ['2026-06-26', 30]]) 

print(lucio.days_origin_dict)
print('-------------------------------')
print(origin)

# push_agent(conn,cursor,lucio)
# push_lisense(conn,cursor, lic1)
# push_lisense(conn,cursor, lic2)
# push_lisense(conn,cursor, lic3)

# delete_license(conn,cursor,lic1)


#connect_end(conn)

