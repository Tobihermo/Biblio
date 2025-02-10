import unittest
from unittest.mock import MagicMock, patch
from negocio.entidades.usuarios.usuario import Usuario
from persistencia.usuariodao import UsuarioDAO
import sqlite3

class TestUsuarioDAO(unittest.TestCase):

    def setUp(self):
        self.db_path = "data/biblioteca.db"
        self.dao = UsuarioDAO()
        self.dao._UsuarioDAO__db_path = self.db_path
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            conn.commit()
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(''' 
                CREATE TABLE IF NOT EXISTS usuarios (
                    id_usuario INTEGER PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    correo TEXT NOT NULL,
                    tipo TEXT NOT NULL
                )
            ''')
            cur.execute("DELETE FROM usuarios WHERE id_usuario > 7") #Para que al correr los tests no se agreguen muchos usuarios
            conn.commit()
    
    def test01_db_path(self):
        self.assertEqual(self.dao.db_path(), "data/biblioteca.db")

    def test02_agregar_usuario(self):
        with sqlite3.connect(self.db_path) as conn:    
            cur = conn.cursor()
            cur.execute("SELECT MAX(id_usuario) + 1 FROM usuarios")
            ultimo_usuario = cur.fetchone()
            ultimo_id = ultimo_usuario[0]
            conn.commit()
        usuario_mock = MagicMock(spec=Usuario)
        usuario_mock.to_dict.return_value = {
            'id_usuario': ultimo_id,
            'nombre': 'Juan Perez',
            'correo': 'juan.perez@example.com',
            'tipo': 'estudiante'
        }
        
        self.dao.agregar_usuario(usuario_mock)
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM usuarios WHERE id_usuario = 1")
            usuario = cur.fetchone()
            self.assertIsNotNone(usuario)
            self.assertEqual(usuario[1], 'Juan Perez')
            self.assertEqual(usuario[2], 'juan.perez@example.com')
            self.assertEqual(usuario[3], 'estudiante')

    def test03_agregar_usuario_con_error(self):
        with sqlite3.connect(self.db_path) as conn:    
            cur = conn.cursor()
            cur.execute("SELECT MAX(id_usuario) FROM usuarios")
            ultimo_usuario = cur.fetchone()
            ultimo_id = ultimo_usuario[0]
            conn.commit()
        usuario_mock = MagicMock(spec=Usuario)
        usuario_mock.to_dict.return_value = {
            'id_usuario': ultimo_id,
            'nombre': 'Benito Benitez',
            'correo': 'benito.benitez@example.com',
            'tipo': 'estudiante'
        }
        with self.assertRaises(sqlite3.IntegrityError):
            self.dao.agregar_usuario(usuario_mock)

    def test04_obtener_usuario(self):
        usuario = self.dao.obtener_usuario(3)
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario['id_usuario'], 3)

    @patch("sqlite3.connect")
    def test05_obtener_usuario_con_error_de_conexion(self, mock_connect):
        with self.assertRaises(sqlite3.Error):
            mock_connect.side_effect = sqlite3.Error("Error en la conexión")
            self.dao.obtener_usuario(1)
    
    def test06_obtener_usuario_con_error_de_id(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT MAX(id_usuario) + 1 FROM usuarios")
            ultimo_usuario = cur.fetchone()
            ultimo_id = ultimo_usuario[0]
            conn.commit()
        usuario = self.dao.obtener_usuario(ultimo_id)
        self.assertIsNone(usuario)

    def test07_obtener_usuario_no_existe(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT MAX(id_usuario) + 1 FROM usuarios")
            ultimo_usuario = cur.fetchone()
            ultimo_id = ultimo_usuario[0]
            conn.commit()
        usuario = self.dao.obtener_usuario(ultimo_id)
        self.assertIsNone(usuario)

    def test08_listar_usuarios(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT MAX(id_usuario) FROM usuarios")
            id_usuario = cur.fetchone()[0]
            id_usuario1 = id_usuario + 1
            id_usuario2 = id_usuario + 2
            cur.execute("INSERT INTO usuarios (id_usuario, nombre, correo, tipo) VALUES (?, ?, ?, ?)", (id_usuario1, 'Gonzalo Gonzalez', 'gonzalez@example.com', 'estudiante'))
            cur.execute("INSERT INTO usuarios (id_usuario, nombre, correo, tipo) VALUES (?, ?, ?, ?)", (id_usuario2, 'Domingo Dominguez', 'domingo.dominguez@example.com', 'profesor'))
            cur.execute("SELECT COUNT(id_usuario) FROM usuarios")
            cantidad_usuarios = cur.fetchone()[0]
            conn.commit()

        usuarios = self.dao.listar_usuarios()
        self.assertEqual(len(usuarios), cantidad_usuarios)
        self.assertEqual(usuarios[-2]['nombre'], 'Gonzalo Gonzalez')
        self.assertEqual(usuarios[-1]['nombre'], 'Domingo Dominguez')
    
    @patch("sqlite3.connect")
    def test09_listar_usuarios_con_error(self, mock_connect):
        with self.assertRaises(sqlite3.Error):
            mock_connect.side_effect = sqlite3.Error("Error en la conexión")
            self.dao.listar_usuarios()

    def test10_eliminar_usuario(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT MAX(id_usuario) + 1 FROM usuarios")
            ultimo_usuario = cur.fetchone()
            ultimo_id = ultimo_usuario[0]
            conn.commit()
            
        self.dao.eliminar_usuario(ultimo_id)
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM usuarios WHERE id_usuario = ?", (ultimo_id,))
            usuario = cur.fetchone()
            self.assertIsNone(usuario)        
    
    @patch("sqlite3.connect")
    def test11_eliminar_usuario_con_error(self, mock_connect):
        mock_connect.side_effect = sqlite3.Error("Error en la conexión")
        with self.assertRaises(sqlite3.Error):
            self.dao.eliminar_usuario(1)

    def test12_obtener_usuario_por_id_tipo_profesor(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT MAX(id_usuario) + 1 FROM usuarios")
            ultimo_usuario = cur.fetchone()
            ultimo_id = ultimo_usuario[0]
            cur.execute("INSERT INTO usuarios (id_usuario, nombre, correo, tipo) VALUES (?, ?, ?, ?)", (ultimo_id, 'Martin Martinez', 'martinez@example.com', 'profesor'))
            conn.commit()

        usuario = self.dao.obtener_usuario_por_id(ultimo_id)
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.id_usuario, ultimo_id)
        self.assertEqual(usuario.nombre, 'Martin Martinez')
    
    def test13_obtener_usuario_por_id_tipo_estudiante(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT MAX(id_usuario) + 1 FROM usuarios")
            ultimo_usuario = cur.fetchone()
            ultimo_id = ultimo_usuario[0]
            cur.execute("INSERT INTO usuarios (id_usuario, nombre, correo, tipo) VALUES (?, ?, ?, ?)", (ultimo_id, 'Gonzalo Gonzalez', 'gonzalez@example.com', 'estudiante'))
            conn.commit()

        usuario = self.dao.obtener_usuario_por_id(ultimo_id)
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.id_usuario, ultimo_id)
        self.assertEqual(usuario.nombre, 'Gonzalo Gonzalez')
    
    def test14_obtener_usuario_por_id_tipo_desconocido(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT MAX(id_usuario) + 1 FROM usuarios")
            ultimo_usuario = cur.fetchone()
            ultimo_id = ultimo_usuario[0]
            cur.execute("INSERT INTO usuarios (id_usuario, nombre, correo, tipo) VALUES (?, ?, ?, ?)", 
                        (ultimo_id, 'Carlos Ruiz', 'carlos.ruiz@example.com', 'administrador'))
            conn.commit()
        usuario = self.dao.obtener_usuario_por_id(ultimo_id)

        self.assertIsNone(usuario)

    @patch("sqlite3.connect")
    def test15_obtener_usuario_por_id_con_error_de_conexion(self, mock_connect):
        mock_connect.side_effect = sqlite3.Error("Error en la conexión")
        with self.assertRaises(sqlite3.Error):
            self.dao.obtener_usuario_por_id(1)

    def test16_obtener_usuarios(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT MAX(id_usuario) + 1 FROM usuarios")
            ultimo_usuario = cur.fetchone()
            ultimo_id = ultimo_usuario[0]
            cur.execute("INSERT INTO usuarios (id_usuario, nombre, correo, tipo) VALUES (?, ?, ?, ?)", (ultimo_id, 'Benito Benitez', 'benitez@example.com', 'estudiante'))
            conn.commit()

        usuarios = self.dao.obtener_usuarios()
        self.assertGreater(len(usuarios), 0)
        self.assertEqual(usuarios[-1]['nombre'], 'Benito Benitez')
        self.assertEqual(usuarios[-1]['correo'], 'benitez@example.com')

    @patch("sqlite3.connect")
    def test17_obtener_usuarios_con_error(self, mock_connect):
        mock_connect.side_effect = sqlite3.Error("Error en la conexión")
        with self.assertRaises(sqlite3.Error):
            self.dao.obtener_usuarios()
    
    def test18_obtener_usuario_por_id_no_existe(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT MAX(id_usuario) + 1 FROM usuarios")
            ultimo_usuario = cur.fetchone()
            ultimo_id = ultimo_usuario[0]
        usuario = self.dao.obtener_usuario_por_id(ultimo_id)
        self.assertIsNone(usuario)
