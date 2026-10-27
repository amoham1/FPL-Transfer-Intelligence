import sqlite3

def load_db(db_path):
    return sqlite3.connect(db_path)

connection = load_db("../database/fpl_data.db")
connection.close()