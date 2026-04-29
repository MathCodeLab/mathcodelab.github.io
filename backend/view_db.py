import sqlite3
conn = sqlite3.connect("app.db")
for row in conn.execute("SELECT * FROM certificates"):
    print(row)
conn.close()