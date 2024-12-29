import sqlite3
from negocio.entidades.reserva import Reserva

class ReservaDAO:
    def __init__(self):
        self.__db_path = "data/biblioteca.db"
        self.__inicializar_db()

    def __inicializar_db(self):
        """
        """
        with sqlite3.connect(self.__db_path) as conn:
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS reservas (
                    id_reserva INTEGER PRIMARY KEY,
                    id_libro INTEGER NOT NULL,
                    id_usuario INTEGER NOT NULL,
                    fecha_reserva TEXT NOT NULL,
                    fecha_devolucion TEXT NOT NULL
                )
            ''')
            conn.commit()


    def agregar_reserva(self, reserva):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                    INSERT INTO reservas (id_libro, id_usuario, fecha_reserva, fecha_devolucion)
                    VALUES (?, ?, ?, ?)
                ''', (
                    reserva.id_libro,
                    reserva.id_usuario,
                    str(reserva.fecha_reserva),  # Asegúrate de que str(fecha_reserva) devuelva el formato correcto
                    str(reserva.fecha_devolucion)
                ))
                conn.commit()
                print("Reserva agregada correctamente.")
        except sqlite3.Error as e:
            print(f"Error al agregar reserva: {e}")
            # Aquí puedes agregar lógica para manejar el error, por ejemplo, registrarlo en un log


    def eliminar_reserva(self, id_reserva):
        """
        """
        try:
            with sqlite3.connect(self.__db_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                    DELETE FROM reservas WHERE id_reserva = ?
                ''', (id_reserva,))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error al eliminar reserva: {e}")

    def listar_reservas(self):
        """
        Obtener todas las reservas de la base de datos.
        """
        try:
            with sqlite3.connect(self.__db_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                    SELECT * FROM reservas
                ''')
                rows = cur.fetchall()
                return [
                    Reserva(row[0], row[1], row[2], row[3], row[4])
                    for row in rows
                ]
        except sqlite3.Error as e:
            print(f"Error al listar reservas: {e}")
            return []

    def obtener_reservas_por_usuario(self, id_usuario):
        """
        Obtener todas las reservas de un usuario en particular.
        """
        try:
            with sqlite3.connect(self.__db_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                    SELECT * FROM reservas WHERE id_usuario = ?
                ''', (id_usuario,))
                rows = cur.fetchall()
                return [
                    Reserva(row[0], row[1], row[2], row[3], row[4])
                    for row in rows
                ]
        except sqlite3.Error as e:
            print(f"Error al obtener reservas por usuario: {e}")
            return []


    def devolver_libro(self, id_reserva):
        """
        Devuelve un libro y elimina la reserva correspondiente.
        """
        try:
            with sqlite3.connect(self.__db_path) as conn:
                cur = conn.cursor()

                # Obtener los detalles de la reserva
                cur.execute('SELECT id_libro FROM reservas WHERE id_reserva = ?', (id_reserva,))
                row = cur.fetchone()
                if row is None:
                    raise ValueError("Reserva no encontrada")
                id_libro = row[0]

                # Eliminar la reserva
                cur.execute('DELETE FROM reservas WHERE id_reserva = ?', (id_reserva,))

                # Actualizar el estado del libro a "disponible"
                cur.execute('UPDATE biblioteca SET estado = "disponible" WHERE id_libro = ?', (id_libro,))

                conn.commit()
                print("Libro devuelto correctamente.")
        except sqlite3.Error as e:
            print(f"Error al devolver el libro: {e}")

    def obtener_libros_disponibles(self, nivel_acceso):
        with sqlite3.connect(self.__db_path) as conn:
            cur = conn.cursor()
            cur.execute('''
                SELECT * FROM biblioteca 
                WHERE estado = "disponible" AND nivel_acceso <= ?
            ''', (nivel_acceso,))
            return cur.fetchall()