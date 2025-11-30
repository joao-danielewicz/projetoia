from objects.Medicamento import Medicamento
from objects.Database import Database
p1 = Medicamento(input("Nome: "),  input("Validade: "))
db = Database()

db.CadastroMedicamento(p1)

print(db.SelectMedicamentos())