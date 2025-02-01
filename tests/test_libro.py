from negocio.entidades.libro import Libro
import unittest

class TestLibro(unittest.TestCase):

    def setUp(self):
        self.libro = Libro(
            id_libro = 1,
            nombre = "Utopía",
            autor = "Thomas More",
            categoria = "Utopía Ficticia",
            estado = "Disponible",
            id_estanteria = 1,
            id_estante = 1,
            nivel_acceso = 1
        )

    def test01_id_libro(self):
        self.assertEqual(self.libro.id_libro, 1)

    def test02_nombre(self):
        self.assertEqual(self.libro.nombre, "Utopía")
        
    def test03_autor(self):
        self.assertEqual(self.libro.autor, "Thomas More")
    
    def test04_categoria(self):
        self.assertEqual(self.libro.categoria, "Utopía Ficticia")
    
    def test05_estado(self):
            self.assertEqual(self.libro.estado, "Disponible")
    
    def test06_id_estanteria(self):
        self.assertEqual(self.libro.id_estanteria, 1)
    
    def test07_id_estante(self):
        self.assertEqual(self.libro.id_estante, 1)

    def test08_nivel_acceso(self):
        self.assertEqual(self.libro.nivel_acceso, 1)

    def test09_actualizar_estado(self):
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

    def test10_to_dict(self):
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