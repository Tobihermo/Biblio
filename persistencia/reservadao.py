import sqlite3
from negocio.entidades.reserva import Reserva
from flask import Flask, render_template, request, redirect, url_for, flash


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

    def get_db(self):
        return sqlite3.connect(self.__db_path)

    def agregar_reserva(self, reserva):
        with sqlite3.connect(self.__db_path) as conn:
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO reservas (id_libro, id_usuario, fecha_reserva, fecha_devolucion)
                VALUES (?, ?, ?, ?)
            ''', (
                reserva.id_libro,
                reserva.id_usuario,
                str(reserva.fecha_reserva),
                str(reserva.fecha_devolucion)
            ))
            conn.commit()
            print("Reserva agregada correctamente.")

    def eliminar_reserva(self, id_reserva):
        """
        """
        with sqlite3.connect(self.__db_path) as conn:
            cur = conn.cursor()
            cur.execute('''
                DELETE FROM reservas WHERE id_reserva = ?
            ''', (id_reserva,))
            conn.commit()

    def listar_reservas(self):
        with self.get_db() as conn:
            reservas = conn.execute('''
                SELECT reservas.id_reserva, biblioteca.id_libro, biblioteca.nombre, biblioteca.autor 
                FROM reservas
                JOIN biblioteca ON reservas.id_libro = biblioteca.id_libro
            ''').fetchall()

        return [
            {
                "id_libro": reserva[1],  # Usamos índices de las tuplas
                "nombre": reserva[2],
                "autor": reserva[3]
            }
            for reserva in reservas
        ]

    def obtener_reservas_por_usuario(self, id_usuario):
        """
        Obtener todas las reservas de un usuario en particular.
        """
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

    def devolver_libro(self, id_reserva):
        with self.get_db() as conn:
            cur = conn.cursor()

            cur.execute('SELECT id_libro FROM reservas WHERE id_reserva = ?', (id_reserva,))
            row = cur.fetchone()
            if not row:
                return False

            id_libro = row[0]
            cur.execute('DELETE FROM reservas WHERE id_reserva = ?', (id_reserva,))
            cur.execute('UPDATE biblioteca SET estado = "disponible" WHERE id_libro = ?', (id_libro,))
            conn.commit()
            return True

    def obtener_libros_disponibles(self, nivel_acceso):
        with sqlite3.connect(self.__db_path) as conn:
            cur = conn.cursor()
            cur.execute('''
                SELECT * FROM biblioteca 
                WHERE estado = "disponible" AND nivel_acceso <= ?
            ''', (nivel_acceso,))
            return cur.fetchall()

    def obtener_historial(self):
        with sqlite3.connect(self.__db_path) as conn:
            conn.row_factory = sqlite3.Row 
            historial = conn.execute(''' 
                SELECT * FROM reservas
                JOIN biblioteca ON reservas.id_libro = biblioteca.id_libro
                JOIN usuarios ON reservas.id_usuario = usuarios.id_usuario
                ORDER BY reservas.fecha_reserva DESC
            ''').fetchall()
            return historial

    def obtener_reserva_por_id_libro(self, id_libro: int):
        with sqlite3.connect(self.__db_path) as conn:
            conn.row_factory = sqlite3.Row 
            reserva = conn.execute('''
                SELECT id_reserva FROM reservas WHERE id_libro = ? ORDER BY id_reserva DESC
            ''', (id_libro,)).fetchone()
            return reserva

    def obtener_max_reserva(self):
        with sqlite3.connect(self.__db_path) as conn:
            max_id = conn.execute('SELECT MAX(id_reserva) FROM reservas').fetchone()[0]
            if max_id is None:
                return 1
            return max_id + 1