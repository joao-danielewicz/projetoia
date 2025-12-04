import os
import numpy as np
from objects.Medicamento import Medicamento
from objects.ConsumoMensal import ConsumoMensal
from objects.Database import Database
from objects.MotorInferencia import MotorInferencia as Motor
from objects.MotorInferencia import *
from datetime import datetime
db = Database()
params = db.SelectParams()


def CalculoMedia(consumos):
    valoresConsumo = []
    for consumo in consumos:
        valoresConsumo.append(consumo[1])
    return (sum(valoresConsumo) / len(valoresConsumo))


def ListarMedicamentos():
    medicamentos = db.SelectMedicamentos()
    print("=========== LISTA DE MEDICAMENTOS ===========")
    for registro in medicamentos:
        medicamento = Medicamento(registro[1], registro[2], registro[3], registro[0])
        medicamento.print()

def ListarConsumos(idMedicamento):
    consumos = db.SelectConsumos(idMedicamento)
    print("=========== LISTA DE CONSUMOS ===========")
    for registro in consumos:
        consumo = ConsumoMensal(registro[1], registro[2], registro[0])
        consumo.print()


while True:
    # ================= MENU GERAL =================
    print("=========== OPÇÕES ===========")
    opcao = int(input("1 - Medicamentos \n 2 - Consumo \n 3 - Editar parâmetros \n 4 - Executar conferências \n 0 - Sair"))
    match opcao:
        case 0:
            break
        case 1:
            os.system('cls')
            # ================= MENU DE MEDICAMENTOS =================
            print("=========== MEDICAMENTOS ===========")
            opcao = int(input("1 - Cadastro \n 2 - Visualizar \n 3 - Ver média de consumo mensal \n4 - Atualizar estoque\n 0 - Voltar"))
            match opcao:
                case 0:
                    break
                case 1:
                    os.system('cls')
                    p1 = Medicamento(input("Nome: "),
                      (
                          datetime(int(input("Validade: \nAno: ")), int(input("Mês: ")), int(input("Dia: ")))
                      ),
                      input("Estoque: "))
                    db.CadastroMedicamento(p1)
                case 2:
                    ListarMedicamentos()
                    input("Pressione qualquer tecla para continuar...'")
                    os.system('cls')
                case 3:
                    ListarMedicamentos()
                    idMedicamento = int(input("Ver média de qual medicamento?"))
                    print(CalculoMedia(db.SelectConsumos(idMedicamento)))
                case 4:
                    ListarMedicamentos()
                    idMedicamento = int(input("Atualizar estoque de qual medicamento?"))
                    db.UpdateEstoqueMedicamento([int(input("Qual o estoque atual?")), idMedicamento])
                    
        case 2:
            os.system('cls')
            # ================= MENU DOS CONSUMOS =================
            print("=========== CONSUMO MENSAL ===========")
            opcao = int(input("1 - Cadastro \n 2 - Visualizar \n 0 - Voltar"))
            match opcao:
                case 0:
                    break;
                case 1:
                    ListarMedicamentos()
                    idMedicamento = int(input("Para qual medicamento deseja cadastrar consumo?"))
                    c1 = ConsumoMensal(int(input("Quantidade: ")), idMedicamento)

                    db.CadastroConsumo(c1)
                case 2:
                    ListarMedicamentos()
                    idMedicamento = int(input("Ver consumos de qual medicamento?"))
                    ListarConsumos(idMedicamento)

        case 3: 
            print("Margem de segurança: ", (params[0]*100),"%\nIntervalo de alerta de vencimento próximo: ", params[1], " dias.")
            print("=========== EDIÇÃO ===========")
            db.UpdateParams([(float(input("Porcentagem da margem de segurança: ")))/100, int(input("\nAlerta de vencimento próximo: "))])
            params = db.SelectParams()

        case 4:
            motor = Motor()
            motor.reset()
            for medicamento in db.SelectMedicamentos():
                consumos = db.SelectConsumos(medicamento[0])
                
                mediaConsumo = CalculoMedia(consumos)
                desvioPadrao = np.std(consumos)

                fator_margem = 1 + (params[0] / 100)

                # Previsão de consumo
                previsao = np.floor((mediaConsumo + desvioPadrao) * fator_margem)

                motor.declare(Estoque(quantidade = medicamento[3], nome = medicamento[1]))
                motor.declare(Previsao(estoque = medicamento[3], nome = medicamento[1], previsao = previsao))
                motor.declare(Validade(data = medicamento[2], nome = medicamento[1]))
                motor.declare(MediaConsumo(media = mediaConsumo, nome = medicamento[1], estoque = medicamento[3], seguranca = params[0]))
            
            motor.run()