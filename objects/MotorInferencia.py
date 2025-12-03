from experta import *


class Estoque(Fact):
    pass

class MotorInferencia(KnowledgeEngine):
    @Rule(Estoque(valor=0, nome = MATCH.nome))
    def estoque_zerado(self, nome):
        print("O estoque de ", nome, "está zerado.")