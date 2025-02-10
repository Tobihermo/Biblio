import unittest
from negocio.entidades.usuarios.usuario import Usuario
from negocio.entidades.usuarios.profesor import Profesor

class TestProfesor(unittest.TestCase):
    def setUp(self):
        self.profesor = Profesor(2, "Pablo Pascal")

    def test01_herencia_usuario(self):
        self.assertIsInstance(self.profesor, Usuario)
    
    def test02_atributos(self):
        self.assertEqual(self.profesor.id_usuario, 2)
        self.assertEqual(self.profesor.nombre, "Pablo Pascal")
        self.assertEqual(self.profesor.tipo, "profesor")
    
    def test03_puede_acceder(self):
        self.assertEqual(self.profesor.puede_acceder(), 2)