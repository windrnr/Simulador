class Process:
    def __init__(self, data: list[int]):
        self._pid = data[0]
        self._size = data[1]
        self._ta = data[2]
        self._ti = data[3]
        self._executing = False

    def return_list_of_data(self) -> list:
        data = []
        data.append(self._pid)
        data.append(self._size)
        data.append(self._ta)
        data.append(self._ti)

        return data

    def get_tiempo_arribo(self) -> int:
        return self._ta

    def get_tamaño(self) -> int:
        return self._size
