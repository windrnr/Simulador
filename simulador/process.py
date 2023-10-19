class Process:
    def __init__(self, data: list[int]):
        self._PID = data[0]
        self._SIZE = data[1]
        self._TA = data[2]
        self._TI = data[3]

    def return_list_of_data(self) -> list:
        data = []
        data.append(self._PID)
        data.append(self._SIZE)
        data.append(self._TA)
        data.append(self._TI)

        return data

    def get_tiempo_arribo(self) -> int:
        return self._TA

    def get_tamaño(self) -> int:
        return self._SIZE
