from negocio.entidades.libro import Libro
from persistencia.librodao import LibroDAO

class GestionLibros:
    def __init__(self):
        self.libro_dao = LibroDAO()

    def validar_disponibilidad(self, id_libro: int) -> bool:
        """
        Verifica si el libro está disponible.
        """
        libro = self.libro_dao.obtener_libro(id_libro)
        if libro and libro['estado'] == "disponible":
            return True
        return False

    def ordenar_libros_por_estanteria(self):
        """
        Ordena los libros por la estantería en la que están.
        """
        libros = self.libro_dao.listar_libros()
        libros_ordenados = sorted(libros, key=lambda x: x['id_estanteria'])
        return libros_ordenados
