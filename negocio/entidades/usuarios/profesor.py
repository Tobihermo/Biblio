from negocio.entidades.usuarios.usuario import Usuario

class Profesor(Usuario):
    """
    Representa el tipo de usuario profesor
    """
    def __init__(self, id_usuario: int, nombre: str):
        super().__init__(id_usuario, nombre, tipo="profesor")

    def puede_acceder(self):
        """
        Cada tipo de usuario tiene acceso a ciertos libros
        """
        return 2