class Fecha:
    def __init__(self, anio: int, mes: int, dia: int):
        """"""
        if not isinstance(anio, int) or not isinstance(mes, int) or not isinstance(dia, int):
            raise TypeError("Error: El año/mes/dia ingresado no son validos")
        if dia > 31 or dia < 0 or mes > 12 or mes < 0:
            raise ValueError("Error: Mes o dia ingresado fuera de rango")
        self.__anio = anio
        self.__mes = mes
        self.__dia = dia

    def __str__(self):
        return f'{self.__dia}/{self.__mes}/{self.__anio}'

    @property
    def fecha(self):
        return (self.__dia, self.__mes, self.__anio)
