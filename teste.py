import numpy as np
class SistemaEspecialista:

  # CÁLCULO DE MÉDIA DE CONSUMO
  def mediaMensal(self, consumo):
      return sum(consumo) / len(consumo)

  # INICIAÇÃO DO SISTEMA E DE VARIÁVEIS DE ARMAZENAMENTO
  def __init__(self):
        self.baseConhecimento = []
        self.produtos = {}
        self.fatos = set()


  # INSERÇÃO DE COJUNTO NA BASE DE CONHECIMENTO
  def regra(self, condicao, conclusao):
    self.baseConhecimento.append((condicao, conclusao))

  # INSERÇÃO DE PRODUTO NO CONJUNTO
  def adicionar_produto(self, produto):
    self.produtos.append(produto)

  # MENU DE CADASTRI DO PRODUTO
  def menuCadastroProduto(self):
    sair = False
    while(sair == False):
      print("O que deseja fazer?")
      opcao = int(input("1 - Adicionar novo produto\n2 - Listar produtos\n0 - Sair"))

      if opcao == 1:
        nomeProduto = input("Digite o nome do produto: ")
        print("Insira os valores de consumo mensais do produto, em sequência dos últimos meses (SOMENTE NÚMEROS).  Digite 'sair' para parar a inserção.")
        consumo = []
        while 1>0:
          try:
            mediaConsumo = int(input());
            if(mediaConsumo > 0):
              consumo.append(mediaConsumo)
          except ValueError:
            break
        print("Desvio padrão: "+str(np.std(consumo)))

        self.produtos.update({nomeProduto : consumo})

      elif opcao == 2:
        print(self.produtos)

      elif opcao == 0:
        sair = True

  # QUESTIONAMENTO AO USUÁRIO A RESPEITO DAS REGRAS APLICADAS.
  # As regras são separadas por assunto. Cada assunto corresponderá a tipos de resposta diferentes,
  # que acarretarão em diversos diagnósticos diferentes.
  def entrada(self, assunto, pergunta, produtoCalc):
    resposta = input(pergunta)
    if assunto == "MEDIA_CONSUMO":
      mediaConsumo = self.mediaMensal(self.produtos[produtoCalc])

      if(int(resposta) > int(mediaConsumo + np.floor((np.std(self.produtos[produtoCalc]))*3))):
        return "acima_media"
      elif(int(resposta) < int(mediaConsumo - np.floor((np.std(self.produtos[produtoCalc]))*3))):
        return "abaixo_media"

    elif (assunto == "ESTOQUE"):
      if(resposta == "cheio"):
        return "nao_abastecer"
      elif(resposta == "vazio"):
        return "abastecer"

  def avaliacao(self):
    applied = True
    while applied:
      applied = False
      for condicao, conclusao in self.baseConhecimento:
        if condicao(self.fatos) and conclusao not in self.fatos:
          print(f"Aplicado a regra: {condicao} -> {conclusao}")
          self.fatos.add(conclusao)
          applied = True

  def run(self):
      self.menuCadastroProduto()
      produtoCalc = input("Qual produto deseja analisar?")
      self.fatos.add(self.entrada("MEDIA_CONSUMO", "Qual foi o consumo deste mês?", produtoCalc))
      self.fatos.add(self.entrada("ESTOQUE", "O estoque está cheio ou vazio?", produtoCalc))
      self.avaliacao()



sistema = SistemaEspecialista()

sistema.regra(lambda fatos: "acima_media" in fatos, "diagnostico: consumo inesperado")
sistema.regra(lambda fatos: "abaixo_media" in fatos, "diagnostico: pouca procura")

sistema.regra(lambda fatos: "abastecer" in fatos, "diagnostico: estoque vazio")
sistema.regra(lambda fatos: "nao_abastecer" in fatos, "diagnostico: estoque em excesso")

if __name__ == "__main__":
  sistema.run()