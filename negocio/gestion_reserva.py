from datetime import datetime
from persistencia.prestamodao import PrestamoDAO
from persistencia.librodao import LibroDAO
from persistencia.usuariodao import UsuarioDAO
from negocio.entidades import Prestamo

class GestionPrestamos:
    def __init__(self):
        pass

    def registrar_reserva(self, id_libro: int, id_usuario: int, fecha: datetime):
        pass

    def registrar_devolucion(self, id_libro: int, fecha: datetime):
        pass

    def ver_historial_reservas(self, id_usuario: int):
        pass
