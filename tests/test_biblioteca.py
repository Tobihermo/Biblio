import unittest
from unittest.mock import MagicMock
from negocio.biblioteca import Biblioteca
from negocio.entidades.libro import Libro
from negocio.entidades.usuarios.usuario import Usuario
from negocio.entidades.reserva import Reserva
from datetime import datetime, timedelta

class TestBiblioteca(unittest.TestCase):

    def setUp(self):
        """
        Método que se ejecuta antes de cada prueba, creando una instancia de Biblioteca.
        """
        self.biblioteca = Biblioteca()
        self.biblioteca.libro_dao = MagicMock()
        self.biblioteca.usuario_dao = MagicMock()
        self.biblioteca.prestamo_dao = MagicMock()

    def test01_agregar_libro(self):
        libro_mock = MagicMock(spec=Libro)
        self.biblioteca.agregar_libro(libro_mock)
        self.biblioteca.libro_dao.agregar_libro.assert_called_once_with(libro_mock)

    def test02_eliminar_libro(self):
        id_libro = 1
        self.biblioteca.eliminar_libro(id_libro)
        self.biblioteca.libro_dao.eliminar_libro.assert_called_once_with(id_libro)

    def test03_buscar_libro_por_id(self):
        libro_data = {
            "id_libro": 1,
            "nombre": "Orgullo y Prejuicio",
            "autor": "Jane Austen",
            "categoria": "Novela Romántica",
            "estado": "disponible",
            "id_estanteria": 1,
            "id_estante": 1,
            "nivel_acceso": 1
        }
        self.biblioteca.libro_dao.obtener_libro.return_value = libro_data
        libro = self.biblioteca.buscar_libro_por_id(1)
        self.assertEqual(libro.nombre, "Orgullo y Prejuicio")
        self.assertEqual(libro.estado, "disponible")

    def test04_prestar_libro(self):
        id_libro = 1
        id_usuario = 1
        libro_mock = MagicMock(spec=Libro)
        libro_mock.estado = "disponible"
        usuario_mock = MagicMock(spec=Usuario)
    
        self.biblioteca.buscar_libro_por_id = MagicMock(return_value=libro_mock)
        self.biblioteca.usuario_dao.obtener_usuario = MagicMock(return_value=usuario_mock)
        self.biblioteca.prestamo_dao.agregar_reserva = MagicMock()
        self.biblioteca.libro_dao.actualizar_estado = MagicMock()

        self.biblioteca.prestamo_dao.listar_reservas = MagicMock(return_value=[MagicMock(id_reserva=1), MagicMock(id_reserva=2)])

        resultado = self.biblioteca.prestar_libro(id_libro, id_usuario)

        self.biblioteca.prestamo_dao.agregar_reserva.assert_called_once()

    def test05_devolver_libro(self):
        id_libro = 1
        libro_mock = MagicMock(spec=Libro)
        libro_mock.estado = "prestado"
        reserva_mock = MagicMock(spec=Reserva)
        reserva_mock.id_libro = id_libro
        reserva_mock.fecha_devolucion = datetime.now() + timedelta(days=1)
        reserva_mock.id_reserva = 2

        self.biblioteca.buscar_libro_por_id = MagicMock(return_value=libro_mock)
        self.biblioteca.prestamo_dao.listar_reservas = MagicMock(return_value=[reserva_mock])
        self.biblioteca.prestamo_dao.eliminar_reserva = MagicMock()
        self.biblioteca.libro_dao.actualizar_estado = MagicMock()

        resultado = self.biblioteca.devolver_libro(id_libro)
        self.assertTrue(resultado)
        self.biblioteca.prestamo_dao.eliminar_reserva.assert_called_once()
        self.biblioteca.libro_dao.actualizar_estado.assert_called_once_with(id_libro, "disponible")

    def test06_listar_libros(self):
        libro_data = [{
            "id_libro": 1,
            "nombre": "Libro Test",
            "autor": "Autor Test",
            "categoria": "Categoria Test",
            "estado": "disponible",
            "id_estanteria": 1,
            "id_estante": 1,
            "nivel_acceso": "publico"
        }]
        self.biblioteca.libro_dao.listar_libros.return_value = libro_data
        libros = self.biblioteca.listar_libros()
        self.assertEqual(len(libros), 1)
        self.assertEqual(libros[0].nombre, "Libro Test")
