import unittest
from unittest.mock import MagicMock
from datetime import datetime
from negocio.entidades.libro import Libro
from negocio.entidades.reserva import Reserva
from negocio.gestion_reserva import GestionBiblioteca

class TestGestionBiblioteca(unittest.TestCase):
    def setUp(self):
        self.gestion_biblioteca = GestionBiblioteca()
        self.gestion_biblioteca.libro_dao = MagicMock()
        self.gestion_biblioteca.usuario_dao = MagicMock()
        self.gestion_biblioteca.reserva_dao = MagicMock()

    def test01_registrar_libro(self):
        id_libro = 1
        nombre = "Harry Potter y la piedra filosofal"
        autor = "J.K. Rowling"
        categoria = "Fantasía"
        estado = "disponible"
        id_estanteria = 1
        id_estante = 1
        nivel_acceso = 1
        
        self.gestion_biblioteca.registrar_libro(id_libro, nombre, autor, categoria, estado, id_estanteria, id_estante, nivel_acceso)
        
        self.gestion_biblioteca.libro_dao.agregar_libro.assert_called_once()

    def test02_eliminar_libro(self):
        id_libro = 1
        
        self.gestion_biblioteca.eliminar_libro(id_libro)
        
        self.gestion_biblioteca.libro_dao.eliminar_libro.assert_called_once_with(id_libro)

    def test03_registrar_usuario(self):
        id_usuario = 1
        nombre = "Juan Perez"
        tipo = "estudiante"
        
        self.gestion_biblioteca.registrar_usuario(id_usuario, nombre, tipo)
        
        self.gestion_biblioteca.usuario_dao.agregar_usuario.assert_called_once()

    def test04_eliminar_usuario(self):
        id_usuario = 1
        
        self.gestion_biblioteca.eliminar_usuario(id_usuario)
        
        self.gestion_biblioteca.usuario_dao.eliminar_usuario.assert_called_once_with(id_usuario)

    def test05_registrar_reserva(self):
        id_libro = 1
        id_usuario = 1
        fecha_reserva = datetime(2025, 1, 10)
        fecha_devolucion = datetime(2025, 1, 17)
        
        self.gestion_biblioteca.registrar_reserva(id_libro, id_usuario, fecha_reserva, fecha_devolucion)
        
        self.gestion_biblioteca.reserva_dao.agregar_reserva.assert_called_once()

    def test06_eliminar_reserva(self):
        id_reserva = 1
        
        self.gestion_biblioteca.eliminar_reserva(id_reserva)
        
        self.gestion_biblioteca.reserva_dao.eliminar_reserva.assert_called_once_with(id_reserva)

    def test07_ver_historial_reservas(self):
        id_usuario = 1
        reservas_mock = [MagicMock(spec=Reserva)]
        self.gestion_biblioteca.reserva_dao.obtener_reservas_por_usuario.return_value = reservas_mock
        
        reservas = self.gestion_biblioteca.ver_historial_reservas(id_usuario)
        
        self.gestion_biblioteca.reserva_dao.obtener_reservas_por_usuario.assert_called_once_with(id_usuario)
        self.assertEqual(reservas, reservas_mock)

    def test08_obtener_estado_libro(self):
        id_libro = 1
        libro_mock = MagicMock(spec=Libro)
        libro_mock.estado = 'disponible'
        
        self.gestion_biblioteca.libro_dao.obtener_libro.return_value = libro_mock
        
        estado = self.gestion_biblioteca.obtener_estado_libro(id_libro)
        
        self.gestion_biblioteca.libro_dao.obtener_libro.assert_called_once_with(id_libro)
        self.assertEqual(estado, 'disponible')
    
    def test09_obtener_estado_libro_no_existente(self):
        self.gestion_biblioteca.libro_dao.obtener_libro.return_value = None

        estado = self.gestion_biblioteca.obtener_estado_libro(999)

        self.assertIsNone(estado)
        self.gestion_biblioteca.libro_dao.obtener_libro.assert_called_once_with(999)

    def test10_generar_id_reserva(self):
        reservas_mock = [MagicMock(spec=Reserva), MagicMock(spec=Reserva)]
        self.gestion_biblioteca.reserva_dao.listar_reservas.return_value = reservas_mock
        
        id_reserva = self.gestion_biblioteca._generar_id_reserva()
        
        self.assertEqual(id_reserva, 3)