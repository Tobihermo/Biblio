import unittest
import sqlite3
from unittest.mock import patch
from persistencia.librodao import LibroDAO
from negocio.entidades.libro import Libro

class TestLibroDAO(unittest.TestCase):

    def setUp(self):
        """ Configura el entorno antes de cada prueba """
        self.dao = LibroDAO()
        self.libro = Libro(
            id_libro=1,
            nombre="Harry Potter y la piedra filosofal",
            autor="J.K. Rowling",
            categoria="Fantasía",
            estado="Disponible",
            id_estanteria=1,
            id_estante=1,
            nivel_acceso=2
        )

    def test01_agregar_libro(self):
        """ Prueba de la función agregar_libro """
        self.dao.agregar_libro(self.libro)
        libro_obtenido = self.dao.obtener_libro(self.libro.id_libro)
        self.assertIsNotNone(libro_obtenido)
        self.assertEqual(libro_obtenido['id_libro'], self.libro.id_libro)

    def test02_obtener_libros_sin_filtro(self):
        p_biblioteca_mock = unittest.mock.Mock()
        p_biblioteca_mock.listar_libros.return_value = []
        libros = self.dao.obtener_libros(p_biblioteca_mock)
        self.assertEqual(libros, [])
    
    @patch('sqlite3.connect')
    @patch.object(LibroDAO, '_LibroDAO__inicializar_db', lambda x: None)
    def test03_obtener_libro_error(self, mock_connect):
        mock_connect.side_effect = sqlite3.Error(f"Error al obtener libro")
        dao = LibroDAO()
        resultado = dao.obtener_libro(1)
        self.assertIsNone(resultado)

    def test04_listar_libros(self):
        """ Prueba de la función listar_libros """
        self.dao.agregar_libro(self.libro)
        libros = self.dao.listar_libros()
        self.assertGreater(len(libros), 0)
        self.assertEqual(libros[0]['id_libro'], self.libro.id_libro)
    
    @patch('sqlite3.connect')
    @patch.object(LibroDAO, '_LibroDAO__inicializar_db', lambda x: None)
    def test05_listar_libros_error(self, mock_connect):
        mock_connect.side_effect = sqlite3.Error("Error al listar libros")
        dao = LibroDAO()
        result = dao.listar_libros()
        self.assertEqual(result, [])

    def test06_eliminar_libro(self):
        """ Prueba de la función eliminar_libro """
        self.dao.agregar_libro(self.libro)
        self.dao.eliminar_libro(self.libro.id_libro)
        libro_obtenido = self.dao.obtener_libro(self.libro.id_libro)
        self.assertIsNone(libro_obtenido)
    
    @patch('sqlite3.connect')
    @patch.object(LibroDAO, '_LibroDAO__inicializar_db', lambda x: None)
    def test07_eliminar_libro_error(self, mock_connect):
        mock_connect.side_effect = sqlite3.Error("Error al eliminar libro")
        dao = LibroDAO()
        dao.eliminar_libro(1)

    def test08_actualizar_estado(self):
        """ Prueba de la función actualizar_estado """
        self.dao.agregar_libro(self.libro)
        self.dao.actualizar_estado(self.libro.id_libro, "prestado")
        libro_obtenido = self.dao.obtener_libro(self.libro.id_libro)
        self.assertEqual(libro_obtenido['estado'], "prestado")
    
    @patch('sqlite3.connect')
    @patch.object(LibroDAO, '_LibroDAO__inicializar_db', lambda x: None)
    def test09_actualizar_estado_error(self, mock_connect):
        mock_connect.side_effect = sqlite3.Error("Error al actualizar estado del libro")
        dao = LibroDAO()
        dao.actualizar_estado(1, "prestado")

    @patch('sqlite3.connect')
    @patch.object(LibroDAO, '_LibroDAO__inicializar_db', lambda x: None)
    def test10_obtener_libros_con_filtro(self, mock_connect):
        """ Prueba de la función obtener_libros con un filtro de búsqueda """
        libros = self.dao.obtener_libros(None, "J.K. Rowling")
        
        self.assertEqual(len(libros), 2)
        self.assertEqual(libros[0]["nombre"], "Harry Potter y la piedra filosofal")
        self.assertEqual(libros[1]["nombre"], "Harry Potter")

