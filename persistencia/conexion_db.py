import sqlite3

class Conexion_Db:
    def get_db(self):
        ''''''
        conn = sqlite3.connect('data/biblioteca.db')
        conn.row_factory = sqlite3.Row
        return conn