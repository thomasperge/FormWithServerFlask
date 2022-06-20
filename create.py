# ----------------------------------------
# Imports / Setup
import sqlite3

connection = sqlite3.connect("DataBase.db")
cursor = connection.cursor()
# ----------------------------------------
# Queries

command = """CREATE TABLE IF NOT EXISTS users(name TEXT, password TEXT)"""

cursor.execute(command)