from negocio.fecha import Fecha

class Reserva:
    def __init__(self, id_reserva: int, id_libro: int, id_usuario: int, fecha_reserva: Fecha, fecha_devolucion: Fecha):
        self.__id_reserva = id_reserva
        self.__id_libro = id_libro
        self.__id_usuario = id_usuario
        self.__fecha_reserva = fecha_reserva
        self.__fecha_devolucion = fecha_devolucion

    def to_dict(self):
        return {
            'id_reserva': self.__id_reserva,
            'id_libro': self.__id_libro,
            'id_usuario': self.__id_usuario,
            'fecha_reserva': self.__fecha_reserva,
            'fecha_devolucion': self.__fecha_devolucion
        }