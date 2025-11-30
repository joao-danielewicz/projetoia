class Medicamento:
    def __init__(self,nome, validade, id=0):
        self.id = id
        self.nome = nome
        self.validade = validade

    def print(self):
        print("ID: ", self.id)
        print("Nome: ", self.nome)
        print("Validade: ", self.validade)
        
