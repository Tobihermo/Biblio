class Estanteria:
    def __init__(self, id_estanteria: int, sector: str):
        self.__id_estanteria = id_estanteria
        self.__sector = sector
        self.__estantes = []

    def agregar_estante(self, estante):
        self.__estantes.append(estante)

    def eliminar_estante(self, estante):
        if estante in self.__estantes:
            self.__estantes.remove(estante)

    def to_dict(self):
        return {
            "id_estanteria": self.__id_estanteria,
            "sector": self.__sector,
            "estantes": [estante.to_dict() for estante in self.__estantes]
        }

    @property
    def id_estanteria(self):
        return self.__id_estanteria

    @property
    def sector(self):
        return self.__sector

    @property
    def estantes(self):
        return self.__estantes
