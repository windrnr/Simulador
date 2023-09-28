class Process:
    def __init__(self, data: list[str]):
        self.PID    = data[0]
        self.SIZE   = data[1]
        self.TA     = data[2]
        self.TI     = data[3]

    def return_list_of_data(self) -> list:
        data = []
        data.append(self.PID)
        data.append(self.SIZE)
        data.append(self.TA)
        data.append(self.TI)

        return data

