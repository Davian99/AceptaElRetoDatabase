import sqlite3
conn = sqlite3.connect('F:\Acepta el reto Database\Envios.db')

c = conn.cursor()

c.execute("SELECT * FROM ENVIOS")

for r in c:
    print(r[4])