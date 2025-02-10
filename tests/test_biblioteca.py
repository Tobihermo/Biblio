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
        self.biblioteca.libro_dao.agregar_libro = MagicMock()
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
    
    def test04_buscar_libro_por_id_no_existe(self):
        self.biblioteca.libro_dao.obtener_libro = MagicMock(return_value=None)
        resultado = self.biblioteca.buscar_libro_por_id(999)
        self.assertIsNone(resultado)

    def test05_prestar_libro(self):
        id_libro = 1
        id_usuario = 1
        libro_mock = MagicMock(spec=Libro)
        libro_mock.estado = "disponible"
        usuario_mock = MagicMock(spec=Usuario)

        self.biblioteca.buscar_libro_por_id = MagicMock(return_value=libro_mock)
        self.biblioteca.usuario_dao.obtener_usuario = MagicMock(return_value=usuario_mock)
        self.biblioteca.prestamo_dao.agregar_reserva = MagicMock()
        self.biblioteca.libro_dao.actualizar_estado = MagicMock()

        self.biblioteca.prestar_libro(id_libro, id_usuario)

        self.biblioteca.prestamo_dao.agregar_reserva.assert_called_once()
        self.biblioteca.libro_dao.actualizar_estado.assert_called_once_with(id_libro, "prestado")

    def test06_prestar_dos_libros(self):
        id_libro1 = 1
        id_libro2 = 2
        id_usuario = 1
        
        libro_mock1 = MagicMock(spec=Libro)
        libro_mock1.estado = "disponible"
        libro_mock2 = MagicMock(spec=Libro)
        libro_mock2.estado = "disponible"
        
        usuario_mock = MagicMock(spec=Usuario)
        
        self.biblioteca.buscar_libro_por_id = MagicMock(side_effect=lambda id_libro: libro_mock1 if id_libro == id_libro1 else libro_mock2)
        self.biblioteca.usuario_dao.obtener_usuario = MagicMock(return_value=usuario_mock)
        self.biblioteca.prestamo_dao.agregar_reserva = MagicMock()
        self.biblioteca.libro_dao.actualizar_estado = MagicMock()
        
        resultado1 = self.biblioteca.prestar_libro(id_libro1, id_usuario)
        resultado2 = self.biblioteca.prestar_libro(id_libro2, id_usuario)
        
        self.assertTrue(resultado1)
        self.assertTrue(resultado2)
        
        self.assertEqual(self.biblioteca.prestamo_dao.agregar_reserva.call_count, 2)
        self.biblioteca.libro_dao.actualizar_estado.assert_any_call(id_libro1, "prestado")
        self.biblioteca.libro_dao.actualizar_estado.assert_any_call(id_libro2, "prestado")

    def test07_prestar_libro_falla(self):
        self.biblioteca.buscar_libro_por_id = MagicMock(return_value=None)
        self.biblioteca.usuario_dao.obtener_usuario = MagicMock(return_value=None)
        resultado = self.biblioteca.prestar_libro(1, 1)
        self.assertFalse(resultado)

    def test08_devolver_libro(self):
        id_libro = 1
        libro_mock = MagicMock(spec=Libro)
        libro_mock.estado = "prestado"
        reserva_mock = MagicMock(spec=Reserva)
        reserva_mock.id_libro = id_libro
        reserva_mock.fecha_devolucion = None
        reserva_mock.id_reserva = 2

        self.biblioteca.buscar_libro_por_id = MagicMock(return_value=libro_mock)
        self.biblioteca.prestamo_dao.listar_reservas = MagicMock(return_value=[reserva_mock])
        self.biblioteca.prestamo_dao.eliminar_reserva = MagicMock()
        self.biblioteca.libro_dao.actualizar_estado = MagicMock()

        resultado = self.biblioteca.devolver_libro(id_libro)
        self.assertTrue(resultado)
        self.biblioteca.prestamo_dao.eliminar_reserva.assert_called_once()
        self.biblioteca.libro_dao.actualizar_estado.assert_called_once_with(id_libro, "disponible")
    
    def test09_devolver_libro_no_existente(self):
        self.biblioteca.libro_dao.obtener_libro.return_value = None
        
        resultado = self.biblioteca.devolver_libro(999)
        
        self.assertFalse(resultado)


    def test10_listar_libros(self):
        libro_data = [{
            "id_libro": 1,
            "nombre": "Utopía",
            "autor": "Thomas More",
            "categoria": "Utopía Ficticia",
            "estado": "Disponible",
            "id_estanteria": 1,
            "id_estante": 1,
            "nivel_acceso": 1
        }]
        self.biblioteca.libro_dao.listar_libros.return_value = libro_data
        libros = self.biblioteca.listar_libros()
        self.assertEqual(len(libros), 1)
        self.assertEqual(libros[0].nombre, "Utopía")
    
    def test11_listar_libros_vacio(self):
        self.biblioteca.libro_dao.listar_libros = MagicMock(return_value=[])

        resultado = self.biblioteca.listar_libros()
        self.assertEqual(resultado, [])
    
    def test12_listar_usuarios(self):
        usuarios_mock = [
            {"id_usuario": 1, "nombre": "Juan Perez", "tipo": "estudiante"},
            {"id_usuario": 2, "nombre": "Pablo Pascal", "tipo": "profesor"}
        ]
        self.biblioteca.usuario_dao.listar_usuarios.return_value = usuarios_mock
        
        usuarios = self.biblioteca.listar_usuarios()
        
        self.biblioteca.usuario_dao.listar_usuarios.assert_called_once()
        
        self.assertEqual(len(usuarios), 2)
        self.assertEqual(usuarios[0].nombre, "Juan Perez")
        self.assertEqual(usuarios[1].nombre, "Pablo Pascal")

