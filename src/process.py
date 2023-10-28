class Proceso:
    def __init__(self, data: list[int]):
        self._pid = data[0]
        self._tamaño = data[1]
        self._tiempo_arribo = data[2]
        self._tiempo_irrupcion = data[3]
        self._ejecutando = False

    def return_list_of_data(self) -> list:
        data = []
        data.append(self._pid)
        data.append(self._tamaño)
        data.append(self._tiempo_arribo)
        data.append(self._tiempo_irrupcion)

        return data

    def get_tiempo_arribo(self) -> int:
        return self._tiempo_arribo

    def get_tamaño(self) -> int:
        return self._tamaño
