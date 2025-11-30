import sqlite3
from objects.Medicamento import Medicamento

class Database:
    
    def __init__(self):
        self.con = sqlite3.connect(".\\database.db")
        self.cur = self.con.cursor()

        res = self.cur.execute("SELECT name FROM sqlite_master WHERE name='medicamento'")
        if (res.fetchone() is None):
            print("Banana")
            self.cur.execute("CREATE TABLE medicamento(nome TEXT, validade DATETIME)")

        res = self.cur.execute("SELECT name FROM sqlite_master")
        print(res.fetchone())
    
    def CadastroMedicamento(self, medicamento):
        dados = [medicamento.nome, medicamento.validade]
        self.cur.execute("INSERT INTO medicamento VALUES(?, ?)", dados)
        self.con.commit()
    
    def SelectMedicamentos(self):
        res = self.cur.execute("SELECT rowid, * FROM medicamento")
        return res.fetchall()