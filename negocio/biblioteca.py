from datetime import datetime
from negocio.entidades import Libro, Usuario, Prestamo
from persistencia.librodao import LibroDAO
from persistencia.usuariodao import UsuarioDAO
from persistencia.prestamodao import PrestamoDAO

class Biblioteca:
    def __init__(self):
        self.libro_dao = LibroDAO()
        self.usuario_dao = UsuarioDAO()
        self.prestamo_dao = PrestamoDAO()

    def agregar_libro(self, libro: Libro):
        pass

    def eliminar_libro(self, id_libro: int):
        pass

    def buscar_libro_por_id(self, id_libro: int):
        pass
    def prestar_libro(self, id_libro: int, id_usuario: int):
        pass

    def devolver_libro(self, id_libro: int):
       pass

    def listar_libros(self):
        pass

    def listar_usuarios(self):
        pass
