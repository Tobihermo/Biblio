import sqlite3
from negocio.entidades.reserva import Reserva

class ReservaDAO:
    def __init__(self):
        self.__db_path = "data/reservas.db"
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
        """
        """
        try:
            with sqlite3.connect(self.__db_path) as conn:
                cur = conn.cursor()
                cur.execute('''
                    INSERT INTO reservas (id_reserva, id_libro, id_usuario, fecha_reserva, fecha_devolucion)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    reserva.to_dict()['id_reserva'],
                    reserva.to_dict()['id_libro'],
                    reserva.to_dict()['id_usuario'],
                    reserva.to_dict()['fecha_reserva'],
                    reserva.to_dict()['fecha_devolucion']
                ))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error al agregar reserva: {e}")

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
