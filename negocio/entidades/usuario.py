class Usuario:    

    def __init__(self, id_usuario, nombre, tipo):
        pass
    def puede_acceder(self, libro):
        pass

    def to_dict(self):
        pass
    @property
    def id_usuario(self):
        return self.__id_usuario

    @property
    def nombre(self):
        return self.__nombre

    @property
    def tipo(self):
        return self.__tipo