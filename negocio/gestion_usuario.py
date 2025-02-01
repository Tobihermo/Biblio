from persistencia.usuariodao import UsuarioDAO
import sqlite3

class GestionUsuarios:
    def __init__(self):
        self.__usuario_dao = UsuarioDAO()
    def validar_acceso(self, id_usuario: int, id_libro: int) -> bool:
        """
        Verifica si un usuario tiene acceso a un libro determinado.
        """
        try:
            # Conectar a la base de datos
            with sqlite3.connect(self.__usuario_dao.db_path) as conn:
                cur = conn.cursor()

                cur.execute('''
                    SELECT 1 FROM accesos WHERE id_usuario = ? AND id_libro = ?
                ''', (id_usuario, id_libro))
                result = cur.fetchone()

                if result:
                    return True
                return False
        except sqlite3.Error as e:
            print(f"Error al validar acceso: {e}")
            return False
