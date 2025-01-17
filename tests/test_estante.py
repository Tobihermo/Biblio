import unittest
from negocio.entidades.libro import Libro
from negocio.entidades.estante import Estante

class TestEstante(unittest.TestCase):

    def test01_creacion_estante(self):
        estante = Estante(1)
        self.assertEqual(estante.id_estante, 1)
        self.assertEqual(estante.libros, [])

    def test02_agregar_libro(self):
        estante = Estante(1)
        libro = Libro(
            id_libro = 1,
            nombre="Harry Potter y la piedra filosofal",
            autor="J.K. Rowling",
            categoria="Fantasía",
            estado="Disponible",
            id_estanteria = 2,
            id_estante = 1,
            nivel_acceso = 1
        )
        estante.agregar_libro(libro)
        self.assertIn(libro, estante.libros)

    def test03_eliminar_libro_existente(self):
        estante = Estante(1)
        libro = Libro(
            id_libro = 1,
            nombre = "Harry Potter y la piedra filosofal",
            autor = "J.K. Rowling",
            categoria = "Fantasía",
            estado = "Disponible",
            id_estanteria = 2,
            id_estante = 1,
            nivel_acceso = 1
        )
        estante.agregar_libro(libro)
        estante.eliminar_libro(libro)
        self.assertNotIn(libro, estante.libros)

    def test04_eliminar_libro_inexistente(self):
        estante = Estante(1)
        libro1 = Libro(
            id_libro = 1,
            nombre = "Harry Potter y la piedra filosofal",
            autor = "J.K. Rowling",
            categoria = "Fantasía",
            estado = "Disponible",
            id_estanteria = 2,
            id_estante = 1,
            nivel_acceso = 1
        )
        libro2 = Libro(
            id_libro = 2,
            nombre = "Orgullo y prejuicio",
            autor = "Jane Austen",
            categoria = "Novela Romantica",
            estado = "Disponible",
            id_estanteria = 3,
            id_estante = 1,
            nivel_acceso = 2
        )
        estante.agregar_libro(libro1)
        estante.eliminar_libro(libro2)
        self.assertIn(libro1, estante.libros)
        self.assertNotIn(libro2, estante.libros)

    def test05_to_dict(self):
        estante = Estante(1)
        libro1 = Libro(
            id_libro = 1,
            nombre = "Harry Potter y la piedra filosofal",
            autor = "J.K. Rowling",
            categoria = "Fantasía",
            estado = "Disponible",
            id_estanteria = 2,
            id_estante = 1,
            nivel_acceso = 1
        )
        
        estante.agregar_libro(libro1)
        estante_dict = estante.to_dict()
        self.assertEqual(estante_dict, {
            "id_estante": 1,
            "libros": [
                {
                    "id_libro": 1,
                    "nombre": "Harry Potter y la piedra filosofal",
                    "autor": "J.K. Rowling",
                    "categoria": "Fantasía",
                    "estado": "Disponible",
                    "id_estanteria": 2,
                    "id_estante": 1,
                    "nivel_acceso": 1
                },
            ]
        })
