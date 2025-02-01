import datetime
from negocio.entidades.libro import Libro
from negocio.entidades.usuarios.usuario import Usuario
from negocio.entidades.reserva import Reserva
from persistencia.librodao import LibroDAO
from persistencia.usuariodao import UsuarioDAO
from persistencia.reservadao import ReservaDAO


class Biblioteca:
    def __init__(self):
        self.libro_dao = LibroDAO()
        self.usuario_dao = UsuarioDAO()
        self.prestamo_dao = ReservaDAO()

    def agregar_libro(self, libro: Libro):
        """
        Agrega un libro a la biblioteca.
        """
        self.libro_dao.agregar_libro(libro)

    def eliminar_libro(self, id_libro: int):
        """
        Elimina un libro de la biblioteca.
        """
        self.libro_dao.eliminar_libro(id_libro)

    def buscar_libro_por_id(self, id_libro: int):
        """
        Busca un libro por su ID.
        """
        libro_data = self.libro_dao.obtener_libro(id_libro)
        if libro_data:
            return Libro(
                libro_data["id_libro"],
                libro_data["nombre"],
                libro_data["autor"],
                libro_data["categoria"],
                libro_data["estado"],
                libro_data["id_estanteria"],
                libro_data["id_estante"],
                libro_data.get("nivel_acceso", None)  # Usa .get() para evitar KeyError
            )
        return None

    def prestar_libro(self, id_libro: int, id_usuario: int):
        libro = self.buscar_libro_por_id(id_libro)
        usuario = self.usuario_dao.obtener_usuario(id_usuario)

        if libro and usuario:
            if libro.estado == "disponible":
                fecha_reserva = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                fecha_devolucion = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')

                # Crear la reserva
                id_reserva = self._generar_id_reserva()
                reserva = Reserva(id_reserva, id_libro, id_usuario, fecha_reserva, fecha_devolucion)

                # Registrar la reserva en la base de datos
                self.prestamo_dao.agregar_reserva(reserva)

                # Cambiar el estado del libro a "prestado"
                self.libro_dao.actualizar_estado(id_libro, "prestado")
                return True

        return False


    def devolver_libro(self, id_libro: int):
        libro = self.buscar_libro_por_id(id_libro)
        if libro:
            reservas = self.prestamo_dao.listar_reservas()
            for reserva in reservas:
                if reserva.id_libro == id_libro and not reserva.fecha_devolucion:
                    self.prestamo_dao.actualizar_fecha_devolucion(reserva.id_reserva, datetime.datetime.now())
                    self.prestamo_dao.eliminar_reserva(reserva.id_reserva)
                    break
            
            # Cambiar el estado del libro a "disponible"
            self.libro_dao.actualizar_estado(id_libro, "disponible")
            return True
        return False

    def listar_libros(self):
        """
        Lista todos los libros de la biblioteca.
        """
        libros_data = self.libro_dao.listar_libros()
        return [
            Libro(
                libro["id_libro"],
                libro["nombre"],
                libro["autor"],
                libro["categoria"],
                libro["estado"],
                libro["id_estanteria"],
                libro["id_estante"],
                libro.get("nivel_acceso", None)
            ) for libro in libros_data
        ]

    def listar_usuarios(self):
        """
        Lista todos los usuarios de la biblioteca.
        """
        usuarios_data = self.usuario_dao.listar_usuarios()
        return [
            Usuario(usuario["id_usuario"], usuario["nombre"], usuario["tipo"])
            for usuario in usuarios_data
        ]

    def _generar_id_reserva(self):
        """
        Genera un nuevo ID de reserva basado en el mayor ID existente en la base de datos,
        utilizando una consulta SQL para mayor eficiencia.
        """
        with self.prestamo_dao.get_db() as conn:
            max_id = conn.execute('SELECT MAX(id_reserva) FROM reservas').fetchone()[0]
            if max_id is None:
                return 1
            return max_id + 1

