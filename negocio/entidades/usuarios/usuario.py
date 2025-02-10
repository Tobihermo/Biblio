class Usuario:
    """
    Representa a un usuario del sistema
    """    
    def __init__(self, id_usuario: int, nombre: str, tipo: str):
        self.__id_usuario = id_usuario
        self.__nombre = nombre
        self.__tipo = tipo
        
    def to_dict(self):
        return {
            'id_usuario': self.__id_usuario,
            'nombre': self.__nombre,
            'tipo': self.__tipo
        }

    @property
    def id_usuario(self):
        return self.__id_usuario

    @property
    def nombre(self):
        return self.__nombre

    @property
    def tipo(self):
        return self.__tipo