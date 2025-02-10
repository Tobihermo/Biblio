import unittest
from negocio.entidades.fecha import Fecha
from negocio.entidades.reserva import Reserva

class TestReserva(unittest.TestCase):

    def test01_creacion_reserva_valida(self):
        fecha_reserva = Fecha(2025, 1, 10)
        fecha_devolucion = Fecha(2025, 1, 20)
        reserva = Reserva(1, 1, 2, fecha_reserva, fecha_devolucion)

        self.assertEqual(reserva.id_reserva, 1)
        self.assertEqual(reserva.id_libro, 1)
        self.assertEqual(reserva.id_usuario, 2)
        self.assertEqual(reserva.fecha_reserva, fecha_reserva)
        self.assertEqual(reserva.fecha_devolucion, fecha_devolucion)

    def test02_to_dict(self):
        fecha_reserva = Fecha(2025, 2, 1)
        fecha_devolucion = Fecha(2025, 2, 15)
        reserva = Reserva(2, 102, 203, fecha_reserva, fecha_devolucion)

        esperado = {
            'id_reserva': 2,
            'id_libro': 102,
            'id_usuario': 203,
            'fecha_reserva': fecha_reserva,
            'fecha_devolucion': fecha_devolucion
        }
        self.assertEqual(reserva.to_dict(), esperado)
