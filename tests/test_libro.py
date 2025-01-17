from negocio.entidades.libro import Libro
import unittest

class TestLibro(unittest.TestCase):

    def test01_creacion_libro_valido(self):
        libro = Libro(
            id_libro = 1,
            nombre = "Utopía",
            autor = "Thomas More",
            categoria = "Utopía Ficticia",
            estado = "prestado",
            id_estanteria = 1,
            id_estante = 1,
            nivel_acceso = 1
        )
        self.assertEqual(libro.nivel_acceso, 1)

    def test02_actualizar_estado(self):
        libro = Libro(
            id_libro=1,
            nombre="1984",
            autor="George Orwell",
            categoria="Ficción",
            estado="Disponible",
            id_estanteria=101,
            id_estante=1,
            nivel_acceso=1
        )
        libro.actualizar_estado("Prestado")
        self.assertEqual(libro.estado, "Prestado")

    def test03_to_dict(self):
        libro = Libro(
            id_libro=1,
            nombre="1984",
            autor="George Orwell",
            categoria="Ficción",
            estado="Disponible",
            id_estanteria=101,
            id_estante=1,
            nivel_acceso=1
        )
        libro_dict = libro.to_dict()
        self.assertEqual(libro_dict, {
            "id_libro": 1,
            "nombre": "1984",
            "autor": "George Orwell",
            "categoria": "Ficción",
            "estado": "Disponible",
            "id_estanteria": 101,
            "id_estante": 1,
            "nivel_acceso": 1
        })