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

class MotorInferenciaAuto(KnowledgeEngine):

    @Rule(Estoque(quantidade=0, nome = MATCH.nome))
    def estoque_zerado(self, nome):
        print("O estoque de ", nome, "está zerado.")


    # VERIFICA SE O ESTOQUE SERÁ SUFICIENTE PARA SUPRIR A POSSÍVEL DEMANDA ESTIMADA
    @Rule(Previsao(estoque=MATCH.estoque, nome=MATCH.nome, previsao = MATCH.previsao), 
          TEST(lambda estoque, previsao: estoque < previsao))              
    def estoque_insatisfatorio(self, nome):
        print("O estoque de ", nome, " é menor do que a previsão estimada. Cuidado!")

    @Rule(Previsao(estoque=MATCH.estoque, nome=MATCH.nome, previsao = MATCH.previsao), 
          TEST(lambda estoque, previsao: estoque > previsao))              
    def estoque_satisfatorio(self, nome):
        print("O estoque de ", nome, " é satisfatório.")
    


    # VERIFICAÇÃO DA DATA DE VALIDADE COM BASE NO PARÂMETRO DEFINIDO.
    @Rule(Validade(data = MATCH.data, nome = MATCH.nome, diasAlerta = MATCH.diasAlerta),
           TEST(lambda data, diasAlerta: ((data - datetime.now()).days) > diasAlerta))
    def risco_vencimento(self, nome, data):
        dias = (data - datetime.now()).days
        print("O medicamento ", nome, " não representa risco de vencimento. ", data)
    
    @Rule(Validade(data = MATCH.data, nome = MATCH.nome, diasAlerta = MATCH.diasAlerta),
           TEST(lambda data, diasAlerta: 1 < ((data - datetime.now()).days) < diasAlerta))
    def risco_vencimento(self, nome, data):
        dias = (data - datetime.now()).days
        print("O medicamento ", nome, " vencerá em ", dias, "dias, na data ", data)

    @Rule(Validade(data = MATCH.data, nome = MATCH.nome),
           TEST(lambda data: ((data - datetime.now()).days) < 1))
    def vencido(self, nome):
        print("O medicamento ", nome, " está vencido! Remova-o do estoque! ")
    
    

    # vERIFICA SE A MÉDIA DE CONSUMO É MENOR OU MAIOR QUE UMA PORCENTAGEM DO ESTOQUE.
    # COM BASE NISSO, INFORMA SE HÁ UM BAIXO OU ALTO CONSUMO
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


class Essencial(Fact):
    pass

class TempoReposicao(Fact):
    pass

class FornecedorAlternativo(Fact):
    pass

class MedicamentoCritico(Fact):
    pass

class MotorInferenciaQuest(KnowledgeEngine):
    # VERIFICA SE UM MEDICAMENTO É ESSENCIAL E SE HÁ FORNECEDOR ALTERNATIVO PARA O MESMO
    @Rule(
        Essencial(nome=MATCH.nome, valor=True),
        FornecedorAlternativo(nome=MATCH.nome, existe=False)
    )
    def prioridade_maxima(self, nome):
        print("PRIORIDADE MÁXIMA para o medicamento", nome)


    # VERIFICA SE HÁ UMA DEMORA NA REPOSIÇÃO DO MEDICAMENTO
    @Rule(
        TempoReposicao(nome=MATCH.nome, dias=MATCH.dias),
        TEST(lambda dias: dias > 20)
    )   
    def reposicao_lenta(self, nome, dias):
        print(f"Atenção: reposição lenta de {nome} ({dias} dias)")

    @Rule(
        Essencial(nome=MATCH.nome, valor=False),
        FornecedorAlternativo(nome=MATCH.nome, existe=True)
    )
    def situacao_confortavel(self, nome):
        print("Medicamento", nome, "em situação confortável")


    # ANALISA SE UM MEDICAMENTO TEM CONSUMO ELEVADO E É DE ATENÇÃO CRÍTICCA.
    @Rule(
        MediaConsumo(nome=MATCH.nome, media=MATCH.media),
        MedicamentoCritico(nome=MATCH.nome, valor=True),
        TEST(lambda media: media > 0)
    )
    def risco_operacional(self, nome):
        print("RISCO OPERACIONAL: medicamento crítico com consumo elevado:", nome)





