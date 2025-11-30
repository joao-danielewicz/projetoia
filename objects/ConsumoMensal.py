class ConsumoMensal:
    def __init__(self, quantidade, idMedicamento, id = 0):
        self.id = id
        self.idMedicamento = idMedicamento
        self.quantidade = quantidade

    def print(self):
        print("ID: ", self.id)
        print("Quantidade: ", self.quantidade)
    