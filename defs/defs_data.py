import sqlite3

conn = sqlite3.connect('./data/dataBase.db')

c = conn.cursor()


# TABLE AGENT
# c.execute("""CREATE TABLE agent (
#             id INTEGRER PRIMARY KEY,
#             cuil TEXT,
#             first TEXT,
#             last TEXT,
#             admission TEXT
#             )""")

# TABLE LICENSES
# c.execute("""CREATE TABLE licenses (
#             id INTEGRER PRIMARY KEY,
#             cuil TEXT,
#             start TEXT,
#             end TEXT,
#             note TEXT
#             )""")

# TABLE days_left
# c.execute("""CREATE TABLE days_left (
#             id INTEGER PRIMARY KEY,
#             cuil TEXT,
#             year_2022 INTEGER,
#             year_2023 INTEGER,
#             year_2024 INTEGER,
#             year_2025 INTEGER,
#             year_2026 INTEGER
#             )""")


# c.execute("INSERT INTO employees VALUES ('Corey','Sanchez', 5000)")

# c.execute("SELECT * FROM employees WHERE last='Sanchez'")

# print(c.fetchone())

conn.commit()

conn.close()