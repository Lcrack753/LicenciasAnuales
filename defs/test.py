from classes import license, agent, days_available
from defs_data import *

lucio = agent('20448919936','Lucio', 'Carnero','01/08/2022')
lic1 = license('20448919936','2021-06-26','2021-07-15','-')
lic2 = license('20448919936','2023-08-06','2023-08-15','-')
lic3 = license('20448919936','2025-01-07','2025-01-20','-')



conn, cursor = connect_start('./data/dataBase.db')
days_lucio = days_available(fetch_license(conn,cursor,'2044',reduce=True),lucio.days_origin_to_tuple())

# print(lucio.days_origin_to_tuple())
print(fetch_license(conn,cursor,'2044',reduce=True))
print(days_lucio.agent_days)
print(days_lucio.to_dict())



# push_agent(conn,cursor,lucio)
# push_lisense(conn,cursor, lic1)
# push_lisense(conn,cursor, lic2)
# push_lisense(conn,cursor, lic3)

# delete_license(conn,cursor,lic1)


connect_end(conn)

