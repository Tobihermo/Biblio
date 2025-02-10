import unittest
import sqlite3
from datetime import datetime
from unittest.mock import patch, MagicMock
from negocio.entidades.reserva import Reserva
from persistencia.reservadao import ReservaDAO

class TestReservaDAO(unittest.TestCase):

    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.db_path = "data/biblioteca.db"
        self.dao = ReservaDAO()
        self.dao._ReservaDAO__db_path = self.db_path
        self.dao._ReservaDAO__inicializar_db()

        self.reserva = Reserva(None, 1, 1, str(datetime.now()), str(datetime.now()))

    def test01_agregar_reserva(self):
        """Test para agregar una reserva."""
        with sqlite3.connect(self.db_path) as conn:    
            cur = conn.cursor()
            cur.execute("SELECT MAX(id_reserva) + 1 FROM reservas")
            nueva_reserva = cur.fetchone()
            reserva_id = nueva_reserva[0]
            cur.execute("SELECT id_libro FROM biblioteca limit 1")
            libro = cur.fetchone()
            libro_id = libro[0]
            cur.execute("SELECT id_usuario FROM usuarios limit 1")
            usuario = cur.fetchone()
            usuario_id = usuario[0]
            conn.commit()
        fecha = str(datetime.now())
        reserva_mock = MagicMock(spec=Reserva)
        reserva_mock.id_reserva = reserva_id
        reserva_mock.id_libro = libro_id
        reserva_mock.id_usuario = usuario_id
        reserva_mock.fecha_reserva = fecha
        reserva_mock.fecha_devolucion = fecha

        self.dao.agregar_reserva(reserva_mock)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM reservas WHERE id_reserva = ?', (reserva_id,))
            reserva = cursor.fetchone()
            print(reserva[1])
            self.assertIsNotNone(reserva)
            self.assertEqual(reserva[1], libro_id)
            self.assertEqual(reserva[2], usuario_id)
            self.assertEqual(reserva[3], fecha)
            self.assertEqual(reserva[4], fecha)

    @patch("sqlite3.connect")
    def test02_agregar_reserva_con_error(self, mock_connect):
        """Test para agregar una reserva y manejar un error en la base de datos."""
        with self.assertRaises(sqlite3.Error):
            mock_connect.side_effect = sqlite3.Error("Error en la conexión")
            self.dao.agregar_reserva(1)

    def test03_eliminar_reserva(self):
        """Test para eliminar una reserva."""
        self.dao.agregar_reserva(self.reserva)
        self.dao.eliminar_reserva(1)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM reservas WHERE id_reserva = 1')
        reserva_db = cursor.fetchone()
        self.assertIsNone(reserva_db, "La reserva no se eliminó correctamente.")
        conn.close()

    def test04_listar_reservas(self):
        """Test para listar las reservas."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(id_reserva) FROM reservas")
            id_reserva = cursor.fetchone()[0]
            id_reserva1 = id_reserva + 1
            id_reserva2 = id_reserva + 2
            fecha = str(datetime.now())
            cursor.execute("INSERT INTO reservas (id_reserva, id_libro, id_usuario, fecha_reserva, fecha_devolucion) VALUES (?, ?, ?, ?, ?)", (id_reserva1, 17, 1, fecha, fecha))
            cursor.execute("INSERT INTO reservas (id_reserva, id_libro, id_usuario, fecha_reserva, fecha_devolucion) VALUES (?, ?, ?, ?, ?)", (id_reserva2, 18, 2, fecha, fecha))
            cursor.execute("SELECT COUNT(id_reserva) FROM reservas")
            cantidad_reservas = cursor.fetchone()[0]
            conn.commit()
        reservas = self.dao.listar_reservas()
        self.assertEqual(len(reservas), cantidad_reservas)
        self.assertEqual(reservas[-2]['id_libro'], 17)
        self.assertEqual(reservas[-1]['id_libro'], 18)
    
    def test05_obtener_reservas_por_usuario(self):
        """Test para obtener las reservas de un usuario."""
        self.dao.agregar_reserva(self.reserva)
        reservas = self.dao.obtener_reservas_por_usuario(1)
        self.assertGreater(len(reservas), 0, "No se pudieron obtener las reservas del usuario.")
    
    @patch("sqlite3.connect")
    def test06_obtener_reservas_por_usuario_con_error_de_conexion(self, mock_connect):
        """Test para obtener reservas por usuario y manejar un error de base de datos."""
        with self.assertRaises(sqlite3.Error):
            mock_connect.side_effect = sqlite3.Error("Error en la conexión")
            self.dao.obtener_reservas_por_usuario(1)
    
    def test07_devolver_libro(self):
        """Test para devolver un libro."""
        with sqlite3.connect(self.db_path) as conn:    
            cur = conn.cursor()
            cur.execute("SELECT MAX(id_reserva) + 1 FROM reservas")
            nueva_reserva = cur.fetchone()
            reserva_id = nueva_reserva[0]
            cur.execute("SELECT id_libro FROM biblioteca limit 1")
            libro = cur.fetchone()
            libro_id = libro[0]
            cur.execute("SELECT id_usuario FROM usuarios limit 1")
            usuario = cur.fetchone()
            usuario_id = usuario[0]
            conn.commit()
        fecha = str(datetime.now())
        reserva_mock = MagicMock(spec=Reserva)
        reserva_mock.id_reserva = reserva_id
        reserva_mock.id_libro = libro_id
        reserva_mock.id_usuario = usuario_id
        reserva_mock.fecha_reserva = fecha
        reserva_mock.fecha_devolucion = fecha

        self.dao.agregar_reserva(reserva_mock)
        self.dao.devolver_libro(reserva_id)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id_reserva FROM reservas WHERE id_reserva = ?', (reserva_id,))
            reserva_id = cursor.fetchone()
            self.assertIsNone(reserva_id)

    def test08_devolver_libro_error(self):
        with sqlite3.connect(self.db_path) as conn:    
            cur = conn.cursor()
            cur.execute("SELECT MAX(id_reserva) + 1 FROM reservas")
            nueva_reserva = cur.fetchone()
            reserva_id = nueva_reserva[0]
            cur.execute("SELECT id_libro FROM biblioteca limit 1")
            libro = cur.fetchone()
            libro_id = libro[0]
            cur.execute("SELECT id_usuario FROM usuarios limit 1")
            usuario = cur.fetchone()
            usuario_id = usuario[0]
            conn.commit()
        fecha = str(datetime.now())
        reserva_mock = MagicMock(spec=Reserva)
        reserva_mock.id_reserva = reserva_id
        reserva_mock.id_libro = libro_id
        reserva_mock.id_usuario = usuario_id
        reserva_mock.fecha_reserva = fecha
        reserva_mock.fecha_devolucion = fecha

        self.dao.agregar_reserva(reserva_mock)
        self.dao.devolver_libro(reserva_id)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id_reserva FROM reservas WHERE id_reserva = ?', (reserva_id,))
            reserva_id = cursor.fetchone()
            self.assertIsNone(reserva_id)

    def test09_obtener_libros_disponibles(self):
        """Test para obtener libros disponibles."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM biblioteca WHERE nivel_acceso <= ? AND estado = ?', (2, 'disponible'))
            libros_disponibles = cursor.fetchone()[0]
            conn.commit()
        
        libros = self.dao.obtener_libros_disponibles(2)

        self.assertGreaterEqual(len(libros), libros_disponibles)

    def test10_obtener_historial(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(id_reserva) FROM reservas")
            id_reserva = cursor.fetchone()[0]
            id_reserva1 = id_reserva + 1
            id_reserva2 = id_reserva + 2
            fecha = str(datetime.now())
            cursor.execute("INSERT INTO reservas (id_reserva, id_libro, id_usuario, fecha_reserva, fecha_devolucion) VALUES (?, ?, ?, ?, ?)", (id_reserva1, 17, 1, fecha, fecha))
            cursor.execute("INSERT INTO reservas (id_reserva, id_libro, id_usuario, fecha_reserva, fecha_devolucion) VALUES (?, ?, ?, ?, ?)", (id_reserva2, 18, 2, fecha, fecha))
            cursor.execute("SELECT COUNT(id_reserva) FROM reservas")
            cantidad_reservas = cursor.fetchone()[0]

            self.assertIsNotNone(id_reserva1)
            self.assertIsNotNone(id_reserva2) 
            reservas = self.dao.obtener_historial()
            self.assertEqual(len(reservas) + 2, (cantidad_reservas))
            cursor.execute("SELECT id_libro, id_usuario FROM reservas WHERE id_reserva=?", (id_reserva1,))
            reserva1 = cursor.fetchone()
            self.assertEqual(reserva1, (17, 1))

            cursor.execute("SELECT id_libro, id_usuario FROM reservas WHERE id_reserva=?", (id_reserva2,))
            reserva2 = cursor.fetchone()
            self.assertEqual(reserva2, (18, 2))
            conn.commit()

    def test11_obtener_reserva_por_id_libro(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(id_reserva) FROM reservas")
            id_reserva = cursor.fetchone()[0]
            id_reserva1 = id_reserva + 1
            id_reserva2 = id_reserva + 2
            fecha = str(datetime.now())
            cursor.execute("INSERT INTO reservas (id_reserva, id_libro, id_usuario, fecha_reserva, fecha_devolucion) VALUES (?, ?, ?, ?, ?)", (id_reserva1, 22, 1, fecha, fecha))
            cursor.execute("INSERT INTO reservas (id_reserva, id_libro, id_usuario, fecha_reserva, fecha_devolucion) VALUES (?, ?, ?, ?, ?)", (id_reserva2, 23, 2, fecha, fecha))
            conn.commit()
            self.assertIsNotNone(id_reserva1)
            self.assertIsNotNone(id_reserva2)
            reserva = self.dao.obtener_reserva_por_id_libro(22)

            self.assertIsNotNone(reserva)
            self.assertEqual(reserva[0], id_reserva1)

    def test12_obtener_max_reserva(self):
        max_reserva = self.dao.obtener_max_reserva()
        self.assertIsInstance(max_reserva, int)
        self.assertGreaterEqual(max_reserva, 0)

    @patch("sqlite3.connect")
    def test13_obtener_max_reserva_sin_reservas(self, mock_connect):
        """Test para obtener el máximo ID de reserva cuando no hay reservas en la base de datos, sin borrar registros reales."""
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.execute.return_value.fetchone.return_value = (None,)
        max_reserva = self.dao.obtener_max_reserva()
        self.assertEqual(max_reserva, 1)

