import sqlite3
from negocio.entidades.usuario import Usuario

class UsuarioDAO:
    def __init__(self):
        self.__db_path = "data/biblioteca.db"
        self.__inicializar_db()

    def __inicializar_db(self):
        """
        """
        with sqlite3.connect(self.__db_path) as conn:
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id_usuario INTEGER PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    tipo TEXT NOT NULL
                )
            ''')
            conn.commit()

    def db_path(self):
        """
        Propiedad que devuelve la ruta de la base de datos.
        """
        return self.__db_path
    def agregar_usuario(self, usuario):
        """
        """
        try:
            with sqlite3.connect(self.__db_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                    INSERT INTO usuarios (id_usuario, nombre, tipo)
                    VALUES (?, ?, ?)
                ''', (
                    usuario.to_dict()['id_usuario'],
                    usuario.to_dict()['nombre'],
                    usuario.to_dict()['tipo']
                ))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error al agregar usuario: {e}")

    def obtener_usuario(self, id_usuario):
        """
        """
        try:
            with sqlite3.connect(self.__db_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                    SELECT * FROM usuarios WHERE id_usuario = ?
                ''', (id_usuario,))
                row = cur.fetchone()
                if row:
                    return {
                        "id_usuario": row[0],
                        "nombre": row[1],
                        "tipo": row[2]
                    }
                return None
        except sqlite3.Error as e:
            print(f"Error al obtener usuario: {e}")
            return None

    def listar_usuarios(self):
        """
        """
        try:
            with sqlite3.connect(self.__db_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                    SELECT * FROM usuarios
                ''')
                rows = cur.fetchall()
                return [
                    {
                        "id_usuario": row[0],
                        "nombre": row[1],
                        "tipo": row[2]
                    } for row in rows
                ]
        except sqlite3.Error as e:
            print(f"Error al listar usuarios: {e}")
            return []

    def eliminar_usuario(self, id_usuario):
        """
        """
        try:
            with sqlite3.connect(self.__db_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                    DELETE FROM usuarios WHERE id_usuario = ?
                ''', (id_usuario,))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error al eliminar usuario: {e}")
