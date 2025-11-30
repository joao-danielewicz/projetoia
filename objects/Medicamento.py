class Medicamento:
    def __init__(self, nome, validade):
        self.id = 0
        self.nome = nome
        self.validade = validade

    def ConstrucaoDatabase(self, id, nome, validade):
        self.id = id
        self.nome = nome
        self.validade = validade


    def print(self):
        print("ID: ", self.id)
        print("Nome: ", self.nome)
        print("Validade: ", self.validade)
        
