class Estante:
    def __init__(self, id_estante: int):
        self.__id_estante = id_estante
        self.__libros = []


    def agregar_libro(self, libro):
        self.__libros.append(libro)

    def eliminar_libro(self, libro):
        if libro in self.__libros:
            self.__libros.remove(libro)

    def to_dict(self):
        return {
            "id_estante": self.__id_estante,
            "libros": [libro.to_dict() for libro in self.__libros]
        }


    @property
    def id_estante(self):
        return self.__id_estante

    @property
    def libros(self):
        return self.__libros