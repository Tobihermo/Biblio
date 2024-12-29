from datetime import datetime
from persistencia.librodao import LibroDAO
from persistencia.usuariodao import UsuarioDAO
from persistencia.reservadao import ReservaDAO
from negocio.entidades.libro import Libro
from negocio.entidades.usuario import Usuario
from negocio.entidades.reserva import Reserva
from negocio.entidades.fecha import Fecha

class GestionBiblioteca:
    def __init__(self):
        # Inicializar los DAO necesarios para manejar libros, usuarios y reservas
        self.libro_dao = LibroDAO()
        self.usuario_dao = UsuarioDAO()
        self.reserva_dao = ReservaDAO()

    # Método para registrar un nuevo libro
    def registrar_libro(self, id_libro, nombre, autor, categoria, estado, id_estanteria, id_estante):
        libro = Libro(id_libro, nombre, autor, categoria, estado, id_estanteria, id_estante)
        self.libro_dao.agregar_libro(libro)

    # Método para eliminar un libro
    def eliminar_libro(self, id_libro):
        self.libro_dao.eliminar_libro(id_libro)

    # Método para registrar un nuevo usuario
    def registrar_usuario(self, id_usuario, nombre, tipo):
        usuario = Usuario(id_usuario, nombre, tipo)
        self.usuario_dao.agregar_usuario(usuario)

    # Método para eliminar un usuario
    def eliminar_usuario(self, id_usuario):
        self.usuario_dao.eliminar_usuario(id_usuario)

    # Método para registrar una nueva reserva
    def registrar_reserva(self, id_libro, id_usuario, fecha_reserva: datetime, fecha_devolucion: datetime):
        fecha_reserva_obj = Fecha(fecha_reserva.year, fecha_reserva.month, fecha_reserva.day)
        fecha_devolucion_obj = Fecha(fecha_devolucion.year, fecha_devolucion.month, fecha_devolucion.day)
        # Asumimos que las reservas son creadas con un ID único incremental, esto se debe adaptar
        id_reserva = self._generar_id_reserva()
        reserva = Reserva(id_reserva, id_libro, id_usuario, fecha_reserva_obj, fecha_devolucion_obj)
        self.reserva_dao.agregar_reserva(reserva)

    # Método para eliminar una reserva
    def eliminar_reserva(self, id_reserva):
        self.reserva_dao.eliminar_reserva(id_reserva)

    # Método para ver el historial de reservas de un usuario
    def ver_historial_reservas(self, id_usuario):
        reservas = self.reserva_dao.obtener_reservas_por_usuario(id_usuario)
        return reservas

    # Método para obtener el estado de un libro
    def obtener_estado_libro(self, id_libro):
        libro = self.libro_dao.obtener_libro(id_libro)
        if libro:
            return libro['estado']
        return None

    # Método privado para generar un ID único para cada reserva (puedes adaptarlo según tu lógica)
    def _generar_id_reserva(self):
        reservas = self.reserva_dao.listar_reservas()  # Este método debería devolver todas las reservas
        return len(reservas) + 1  # Esto es solo un ejemplo, puedes usar un contador o un sistema más robusto
