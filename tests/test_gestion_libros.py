import unittest
from unittest.mock import MagicMock
from negocio.gestion_libros import GestionLibros

class TestGestionLibros(unittest.TestCase):
    def setUp(self):
        """
        Configuración inicial para los tests.
        """
        self.gestion_libros = GestionLibros()
        self.gestion_libros.libro_dao = MagicMock()

    def test01_validar_disponibilidad_libro_disponible(self):
        """
        Verifica que un libro disponible devuelva True.
        """
        libro_data = {"id_libro": 1, "estado": "disponible"}
        self.gestion_libros.libro_dao.obtener_libro.return_value = libro_data

        resultado = self.gestion_libros.validar_disponibilidad(1)
        self.assertTrue(resultado)
        self.gestion_libros.libro_dao.obtener_libro.assert_called_once_with(1)

    def test02_validar_disponibilidad_libro_no_disponible(self):
        """
        Verifica que un libro no disponible devuelva False.
        """
        libro_data = {"id_libro": 1, "estado": "prestado"}
        self.gestion_libros.libro_dao.obtener_libro.return_value = libro_data

        resultado = self.gestion_libros.validar_disponibilidad(1)
        self.assertFalse(resultado)
        self.gestion_libros.libro_dao.obtener_libro.assert_called_once_with(1)

    def test03_validar_disponibilidad_libro_no_existente(self):
        """
        Verifica que un libro inexistente devuelva False.
        """
        self.gestion_libros.libro_dao.obtener_libro.return_value = None

        resultado = self.gestion_libros.validar_disponibilidad(1)
        self.assertFalse(resultado)
        self.gestion_libros.libro_dao.obtener_libro.assert_called_once_with(1)

    def test04_ordenar_libros_por_estanteria(self):
        """
        Verifica que los libros se ordenen correctamente por id_estanteria.
        """
        libros_data = [
            {"id_libro": 1, "id_estanteria": 2},
            {"id_libro": 2, "id_estanteria": 1},
            {"id_libro": 3, "id_estanteria": 3},
        ]
        self.gestion_libros.libro_dao.listar_libros.return_value = libros_data

        resultado = self.gestion_libros.ordenar_libros_por_estanteria()
        libros_esperados = [
            {"id_libro": 2, "id_estanteria": 1},
            {"id_libro": 1, "id_estanteria": 2},
            {"id_libro": 3, "id_estanteria": 3},
        ]
        self.assertEqual(resultado, libros_esperados)
        self.gestion_libros.libro_dao.listar_libros.assert_called_once()