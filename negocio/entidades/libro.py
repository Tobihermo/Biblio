class Libro:
    def __init__(self, id_libro, nombre, autor, categoria, estado, id_estanteria, id_estante, nivel_acceso):
        self.__id_libro = id_libro
        self.__nombre = nombre
        self.__autor = autor
        self.__categoria = categoria
        self.__estado = estado
        self.__id_estanteria = id_estanteria
        self.__id_estante = id_estante
        self.__nivel_acceso = nivel_acceso

    def actualizar_estado(self, nuevo_estado):
        self.__estado = nuevo_estado

    def to_dict(self):
        return {
            "id_libro": self.__id_libro,
            "nombre": self.__nombre,
            "autor": self.__autor,
            "categoria": self.__categoria,
            "estado": self.__estado,
            "id_estanteria": self.__id_estanteria,
            "id_estante": self.__id_estante,
            "nivel_acceso": self.__nivel_acceso
        }

    @property
    def id_libro(self):
        return self.__id_libro

    @property
    def nivel_acceso(self):
        return self.__nivel_acceso

    @property
    def nombre(self):
        return self.__nombre

    @property
    def autor(self):
        return self.__autor

    @property
    def categoria(self):
        return self.__categoria

    @property
    def estado(self):
        return self.__estado

    @property
    def id_estanteria(self):
        return self.__id_estanteria

    @property
    def id_estante(self):
        return self.__id_estante
