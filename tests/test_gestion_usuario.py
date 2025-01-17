import unittest
from unittest.mock import MagicMock, patch
from negocio.gestion_usuario import GestionUsuarios
import sqlite3

class TestGestionUsuarios(unittest.TestCase):
    def setUp(self):
        """
        Configuración inicial para los tests.
        """
        self.gestion_usuarios = GestionUsuarios()
        self.gestion_usuarios._GestionUsuarios__usuario_dao = MagicMock()
        self.mock_db_path = "mock_db.sqlite"
        self.gestion_usuarios._GestionUsuarios__usuario_dao.db_path = self.mock_db_path

    @patch("sqlite3.connect")
    def test01_validar_acceso_usuario_con_acceso(self, mock_connect):
        """
        Verifica que el método devuelve True cuando el usuario tiene acceso.
        """
        mock_conn = mock_connect.return_value.__enter__.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = (1,)

        resultado = self.gestion_usuarios.validar_acceso(1, 101)
        self.assertTrue(resultado)

        mock_connect.assert_called_once_with(self.mock_db_path)
        mock_cursor.execute.assert_called_once_with(
        '''
                    SELECT 1 FROM accesos WHERE id_usuario = ? AND id_libro = ?
                ''', 
        (1, 101))


    @patch("sqlite3.connect")
    def test02_validar_acceso_usuario_sin_acceso(self, mock_connect):
        """
        Verifica que el método devuelve False cuando el usuario no tiene acceso.
        """
        mock_conn = mock_connect.return_value.__enter__.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = None

        resultado = self.gestion_usuarios.validar_acceso(1, 101)
        self.assertFalse(resultado)

        mock_connect.assert_called_once_with(self.mock_db_path)
        mock_cursor.execute.assert_called_once_with(
        '''
                    SELECT 1 FROM accesos WHERE id_usuario = ? AND id_libro = ?
                ''', 
        (1, 101))

    @patch("sqlite3.connect")
    def test03_validar_acceso_error_sqlite(self, mock_connect):
        """
        Verifica que el método devuelve False cuando ocurre un error de SQLite.
        """
        mock_connect.side_effect = sqlite3.Error("Error de conexión")

        resultado = self.gestion_usuarios.validar_acceso(1, 101)
        self.assertFalse(resultado)

        mock_connect.assert_called_once_with(self.mock_db_path)

if __name__ == "__main__":
    unittest.main()
