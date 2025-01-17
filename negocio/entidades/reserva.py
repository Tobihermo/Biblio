from negocio.entidades.fecha import Fecha

class Reserva:
    def __init__(self, id_reserva: int, id_libro: int, id_usuario: int, fecha_reserva: Fecha, fecha_devolucion: Fecha):
        self.id_reserva = id_reserva
        self.id_libro = id_libro
        self.id_usuario = id_usuario
        self.fecha_reserva = fecha_reserva
        self.fecha_devolucion = fecha_devolucion

    def to_dict(self):
        return {
            'id_reserva': self.id_reserva,
            'id_libro': self.id_libro,
            'id_usuario': self.id_usuario,
            'fecha_reserva': self.fecha_reserva,
            'fecha_devolucion': self.fecha_devolucion
        }