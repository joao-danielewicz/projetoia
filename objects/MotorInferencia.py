from experta import *
from datetime import datetime


class Estoque(Fact):
    pass

class MediaConsumo(Fact):
    pass

class Validade(Fact):
    pass

class Previsao(Fact):
    pass

class MotorInferencia(KnowledgeEngine):
    @Rule(Estoque(quantidade=0, nome = MATCH.nome))
    def estoque_zerado(self, nome):
        print("O estoque de ", nome, "está zerado.")



    @Rule(Previsao(estoque=MATCH.estoque, nome=MATCH.nome, previsao = MATCH.previsao), 
          TEST(lambda estoque, previsao: estoque < previsao))              
    def estoque_insatisfatorio(self, nome):
        print("O estoque de ", nome, " é menor do que a previsão estimada. Cuidado!")

    @Rule(Previsao(estoque=MATCH.estoque, nome=MATCH.nome, previsao = MATCH.previsao), 
          TEST(lambda estoque, previsao: estoque > previsao))              
    def estoque_satisfatorio(self, nome):
        print("O estoque de ", nome, " é satisfatório.")
    

    @Rule(Validade(data = MATCH.data, nome = MATCH.nome),
           TEST(lambda data: ((data - datetime.now()).days) > 90))
    def risco_vencimento(self, nome, data):
        dias = (data - datetime.now()).days
        print("O medicamento ", nome, " não representa risco de vencimento. ", data)
    
    @Rule(Validade(data = MATCH.data, nome = MATCH.nome),
           TEST(lambda data: 1 < ((data - datetime.now()).days) < 90))
    def risco_vencimento(self, nome, data):
        dias = (data - datetime.now()).days
        print("O medicamento ", nome, " vencerá em ", dias, "dias, na data ", data)

    @Rule(Validade(data = MATCH.data, nome = MATCH.nome),
           TEST(lambda data: ((data - datetime.now()).days) < 1))
    def vencido(self, nome):
        print("O medicamento ", nome, " está vencido! Remova-o do estoque! ")
    
    
    @Rule(
        MediaConsumo(nome=MATCH.nome, media=MATCH.media, estoque = MATCH.estoque, seguranca = MATCH.seguranca),
        TEST(lambda media, estoque, seguranca: media > estoque*seguranca)
    )
    def alto_consumo(self, nome):
        print("Há um consumo elevado de ", nome)
    
    @Rule(
        MediaConsumo(nome=MATCH.nome, media=MATCH.media, estoque = MATCH.estoque, seguranca = MATCH.seguranca),
        TEST(lambda media, estoque, seguranca: media < estoque*seguranca)
    )
    def baixo_consumo(self, nome):
        print("Há um consumo baixo de ", nome)