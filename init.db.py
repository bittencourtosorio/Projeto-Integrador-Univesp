import sqlite3

connection =sqlite3.connect('base_conhecimento_db.db')

with open ('schema.sql') as f:
    connection.executescript(f.read())

    cursor = connection.cursor()

connection.commit()
connection.close()