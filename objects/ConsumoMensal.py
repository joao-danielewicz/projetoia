class ConsumoMensal:
    def __init__(self, quantidade, idMedicamento):
        self.id = 0
        self.idMedicamento = idMedicamento
        self.quantidade = quantidade

    def ConstrucaoDatabase(self, id, quantidade, idMedicamento):
        self.id = id
        self.quantidade = quantidade
        self.idMedicamento = idMedicamento
    