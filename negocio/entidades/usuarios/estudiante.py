from negocio.entidades.usuarios.usuario import Usuario

class Estudiante(Usuario):
    """
    Representa el tipo de usuario estudiante
    """
    def __init__(self, id_usuario: int, nombre: str):
        super().__init__(id_usuario, nombre, tipo="estudiante")

    def puede_acceder(self):
        """
        Cada tipo de usuario tiene acceso a ciertos libros
        """
        return 1
