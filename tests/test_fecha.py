from negocio.entidades.fecha import Fecha
import unittest

class TestFecha(unittest.TestCase):
    def test01_creacion_fecha_valida(self):
        fecha = Fecha(2023, 12, 31)
        self.assertEqual(fecha.fecha, (31, 12, 2023))
        self.assertEqual(str(fecha), "31/12/2023")
    
    def test02_creacion_fecha_invalida_rango(self):
        with self.assertRaises(ValueError):
            Fecha(2023, 13, 1)
        with self.assertRaises(ValueError):
            Fecha(2023, 12, 32)
        with self.assertRaises(ValueError):
            Fecha(2023, 12, -1)
        
        with self.assertRaises(TypeError):
            Fecha("2023", 12, 31)
        with self.assertRaises(TypeError):
            Fecha(2023, "12", 31)
        with self.assertRaises(TypeError):
            Fecha(2023, 12, "31")