import unittest
from negocio.entidades.estanteria import Estanteria
from negocio.entidades.estante import Estante
from negocio.entidades.libro import Libro

class TestEstanteria(unittest.TestCase):

    def test01_creacion_estanteria(self):
        estanteria = Estanteria(1, "Sector A")
        self.assertEqual(estanteria.id_estanteria, 1)
        self.assertEqual(estanteria.sector, "Sector A")
        self.assertEqual(estanteria.estantes, [])

    def test02_agregar_estante(self):
        estanteria = Estanteria(1, "Sector A")
        estante = Estante(1)
        estanteria.agregar_estante(estante)
        self.assertIn(estante, estanteria.estantes)

    def test03_eliminar_estante_existente(self):
        estanteria = Estanteria(1, "Sector A")
        estante = Estante(1)
        estanteria.agregar_estante(estante)
        estanteria.eliminar_estante(estante)
        self.assertNotIn(estante, estanteria.estantes)

    def test04_eliminar_estante_inexistente(self):
        estanteria = Estanteria(1, "Sector A")
        estante1 = Estante(1)
        estante2 = Estante(2)
        estanteria.agregar_estante(estante1)
        estanteria.eliminar_estante(estante2)
        self.assertIn(estante1, estanteria.estantes)
        self.assertNotIn(estante2, estanteria.estantes)

    def test05_to_dict(self):
        estanteria = Estanteria(1, "Sector A")
        estante1 = Estante(1)
        
        libro1 = Libro(
            id_libro = 1,
            nombre = "Harry Potter y la piedra filosofal",
            autor = "J.K. Rowling",
            categoria = "Fantasía",
            estado = "Disponible",
            id_estanteria = 1,
            id_estante = 1,
            nivel_acceso = 1
        )
        
        estante1.agregar_libro(libro1)
        estanteria.agregar_estante(estante1)

        estanteria_dict = estanteria.to_dict()

        self.assertEqual(estanteria_dict, {
            "id_estanteria": 1,
            "sector": "Sector A",
            "estantes": [
                {
                    "id_estante": 1,
                    "libros": [
                        {
                            "id_libro": 1,
                            "nombre": "Harry Potter y la piedra filosofal",
                            "autor": "J.K. Rowling",
                            "categoria": "Fantasía",
                            "estado": "Disponible",
                            "id_estanteria": 1,
                            "id_estante": 1,
                            "nivel_acceso": 1
                        }
                    ]
                }
            ]
        })
