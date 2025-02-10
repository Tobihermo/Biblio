import unittest
from negocio.entidades.usuarios.usuario import Usuario

class TestUsuario(unittest.TestCase):

    def test01_creacion_usuario_valido(self):
        usuario = Usuario(1, "Juan Perez", "estudiante")
        self.assertEqual(usuario.id_usuario, 1)
        self.assertEqual(usuario.nombre, "Juan Perez")
        self.assertEqual(usuario.tipo, "estudiante")

    def test02_to_dict(self):
        usuario = Usuario(2, "Benito Benitez", "profesor")
        esperado = {
            'id_usuario': 2,
            'nombre': "Benito Benitez",
            'tipo': "profesor"
        }
        self.assertEqual(usuario.to_dict(), esperado)
