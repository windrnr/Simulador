from main import Particion


class Proceso:
    def __init__(self, data: list[int]):
        self.pid = data[0]
        self.tamaño = data[1]
        self.tiempo_arribo = data[2]
        self.tiempo_irrupcion = data[3]
        # self.ejecutando = False
        self.particion = Particion

    def return_list_of_data(self) -> list:
        data = []
        data.append(self.pid)
        data.append(self.tamaño)
        data.append(self.tiempo_arribo)
        data.append(self.tiempo_irrupcion)

        return data

    def get_tiempo_arribo(self) -> int:
        return self.tiempo_arribo

    def get_tamaño(self) -> int:
        return self.tamaño
