import unittest
from negocio.entidades.usuarios.usuario import Usuario
from negocio.entidades.usuarios.estudiante import Estudiante

class TestEstudiante(unittest.TestCase):
    def setUp(self):
        self.estudiante = Estudiante(1, "Juan Perez")

    def test01_herencia_usuario(self):
        self.assertIsInstance(self.estudiante, Usuario)
    
    def test02_atributos(self):
        self.assertEqual(self.estudiante.id_usuario, 1)
        self.assertEqual(self.estudiante.nombre, "Juan Perez")
        self.assertEqual(self.estudiante.tipo, "estudiante")
    
    def test03_puede_acceder(self):
        self.assertEqual(self.estudiante.puede_acceder(), 1)