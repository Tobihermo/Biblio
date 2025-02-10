import sqlite3


class LibroDAO:
    def __init__(self):
        self.__db_path = "data/biblioteca.db"
        self.__inicializar_db()

    def __inicializar_db(self):
        with sqlite3.connect(self.__db_path) as conn:
            cur = conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS biblioteca (
                id_libro INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                autor TEXT NOT NULL,
                categoria TEXT NOT NULL,
                estado TEXT NOT NULL,
                id_estanteria INTEGER NOT NULL,
                id_estante INTEGER NOT NULL,
                nivel_acceso INTEGER NOT NULL
            )''')
            conn.commit()


    def agregar_libro(self, libro):
        """
        """
        try:
            with sqlite3.connect(self.__db_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                    INSERT INTO biblioteca (id_libro, nombre, autor, categoria, estado, id_estanteria, id_estante, nivel_acceso)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    libro.to_dict()['id_libro'],
                    libro.to_dict()['nombre'],
                    libro.to_dict()['autor'],
                    libro.to_dict()['categoria'],
                    libro.to_dict()['estado'],
                    libro.to_dict()['id_estanteria'],
                    libro.to_dict()['id_estante'],
                    libro.to_dict()['nivel_acceso']
                ))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error al agregar libro: {e}")

    def obtener_libro(self, id_libro):
        """
        """
        try:
            with sqlite3.connect(self.__db_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                    SELECT * FROM biblioteca WHERE id_libro = ?
                ''', (id_libro,))
                row = cur.fetchone()
                if row:
                    return {
                        "id_libro": row[0],
                        "nombre": row[1],
                        "autor": row[2],
                        "categoria": row[3],
                        "estado": row[4],
                        "id_estanteria": row[5],
                        "id_estante": row[6],
                        "nivel_acceso": row[7]
                    }
                return None
        except sqlite3.Error as e:
            print(f"Error al obtener libro: {e}")
            return None
    
    def obtener_libros(self, p_biblioteca, query=""):
        with sqlite3.connect(self.__db_path) as conn:
            conn.row_factory = sqlite3.Row  
            if query:
                return conn.execute(''' 
                    SELECT * FROM biblioteca WHERE nombre LIKE ? OR autor LIKE ? 
                ''', (f'%{query}%', f'%{query}%')).fetchall()
            return p_biblioteca.listar_libros()

    def listar_libros(self):
        try:
            with sqlite3.connect(self.__db_path) as conn:
                cur = conn.cursor()
                cur.execute('''SELECT * FROM biblioteca''')
                rows = cur.fetchall()
                return [
                    {"id_libro": row[0], "nombre": row[1], "autor": row[2], "categoria": row[3], "estado": row[4], "id_estanteria": row[5], "id_estante": row[6], "nivel_acceso": row[7]}
                    for row in rows
                ]
        except sqlite3.Error as e:
            print(f"Error al listar libros: {e}")
            return []

    def eliminar_libro(self, id_libro):
        """
        """
        try:
            with sqlite3.connect(self.__db_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                    DELETE FROM biblioteca WHERE id_libro = ?
                ''', (id_libro,))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error al eliminar libro: {e}")

    def actualizar_estado(self, id_libro, nuevo_estado):
        """
        """
        try:
            with sqlite3.connect(self.__db_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                    UPDATE biblioteca SET estado = ? WHERE id_libro = ?
                ''', (nuevo_estado, id_libro))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error al actualizar estado del libro: {e}")
