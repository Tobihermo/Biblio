from datetime import datetime
from persistencia.librodao import LibroDAO
from persistencia.usuariodao import UsuarioDAO
from persistencia.reservadao import ReservaDAO
from negocio.entidades.libro import Libro
from negocio.entidades.usuarios.usuario import Usuario
from negocio.entidades.reserva import Reserva
from negocio.entidades.fecha import Fecha


class GestionBiblioteca:
    def __init__(self):
        """
        Se inicializan los DAO necesarios para manejar libros, usuarios y reservas
        """
        self.libro_dao = LibroDAO()
        self.usuario_dao = UsuarioDAO()
        self.reserva_dao = ReservaDAO()

    def registrar_libro(self, id_libro, nombre, autor, categoria, estado, id_estanteria, id_estante, nivel_acceso):
        libro = Libro(id_libro, nombre, autor, categoria, estado,
                      id_estanteria, id_estante, nivel_acceso)
        self.libro_dao.agregar_libro(libro)

    def eliminar_libro(self, id_libro):
        self.libro_dao.eliminar_libro(id_libro)

    def registrar_usuario(self, id_usuario, nombre, tipo):
        usuario = Usuario(id_usuario, nombre, tipo)
        self.usuario_dao.agregar_usuario(usuario)

    def eliminar_usuario(self, id_usuario):
        self.usuario_dao.eliminar_usuario(id_usuario)

    def registrar_reserva(self, id_libro, id_usuario, fecha_reserva: datetime, fecha_devolucion: datetime):
        fecha_reserva_obj = Fecha(
            fecha_reserva.year, fecha_reserva.month, fecha_reserva.day)
        fecha_devolucion_obj = Fecha(
            fecha_devolucion.year, fecha_devolucion.month, fecha_devolucion.day)
        id_reserva = self._generar_id_reserva()
        reserva = Reserva(id_reserva, id_libro, id_usuario,
                          fecha_reserva_obj, fecha_devolucion_obj)
        self.reserva_dao.agregar_reserva(reserva)

    def eliminar_reserva(self, id_reserva):
        self.reserva_dao.eliminar_reserva(id_reserva)

    def ver_historial_reservas(self, id_usuario):
        reservas = self.reserva_dao.obtener_reservas_por_usuario(id_usuario)
        return reservas

    def obtener_estado_libro(self, id_libro):
        libro = self.libro_dao.obtener_libro(id_libro)
        if libro:
            return libro.estado
        return None

    def _generar_id_reserva(self):
        reservas = self.reserva_dao.listar_reservas()
        return len(reservas) + 1
