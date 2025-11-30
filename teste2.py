from objects.Medicamento import Medicamento
from objects.ConsumoMensal import ConsumoMensal
from objects.Database import Database
db = Database()




while True:
    # ================= MENU GERAL =================
    opcao = int(input("1 - Medicamentos \n 2 - Consumo \n 0 - Sair"))
    match opcao:
        case 0:
            break
        case 1:

            # ================= MENU DE MEDICAMENTOS =================
            opcao = int(input("1 - Cadastro \n 2 - Visualizar \n 0 - Voltar"))
            match opcao:
                case 0:
                    break
                case 1:
                    p1 = Medicamento(input("Nome: "),  input("Validade: "))
                    db.CadastroMedicamento(p1)
                case 2:
                    medicamentos = db.SelectMedicamentos()
                    for registro in medicamentos:
                        medicamento = Medicamento(registro[1], registro[2], registro[0])
                        medicamento.print()
        case 2:
            # ================= MENU DOS CONSUMOS =================
            print(db.SelectMedicamentos())
            c1 = ConsumoMensal(int(input("Quantidade: ")), int(input("ID: ")))
            db.CadastroConsumo(c1)
            


print(db.SelectConsumos(int(input())))