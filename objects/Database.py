import sqlite3
from objects.Medicamento import Medicamento

class Database:
    
    def __init__(self):
        self.con = sqlite3.connect(".\\database.db")
        self.cur = self.con.cursor()

        res = self.cur.execute("SELECT name FROM sqlite_master WHERE name='medicamento'")
        if (res.fetchone() is None):
            self.cur.execute("CREATE TABLE medicamento(nome TEXT, validade DATETIME, estoque INT)")
            
        res = self.cur.execute("SELECT name FROM sqlite_master WHERE name='consumo'")
        if (res.fetchone() is None):
            self.cur.execute("CREATE TABLE consumo(quantidade INT, idMedicamento INT)")

        res = self.cur.execute("SELECT name FROM sqlite_master")
    
    def CadastroMedicamento(self, medicamento):
        dados = [medicamento.nome, medicamento.validade, medicamento.estoque]
        self.cur.execute("INSERT INTO medicamento VALUES(?, ?, ?)", dados)
        self.con.commit()
    
    def SelectMedicamentos(self):
        res = self.cur.execute("SELECT rowid, * FROM medicamento")
        return res.fetchall()
    
    def UpdateEstoqueMedicamento(self, dados):
        self.cur.execute("UPDATE medicamento SET estoque = ? WHERE rowid = ?", dados)
        self.con.commit()
    
    
    def CadastroConsumo(self, consumo):
        dados = [consumo.quantidade, consumo.idMedicamento]
        self.cur.execute("INSERT INTO consumo VALUES(?, ?)", dados)
        self.con.commit()

    def SelectConsumos(self, idMedicamento):
        res = self.cur.execute("SELECT rowid, * FROM consumo WHERE idMedicamento = ?", (idMedicamento,))
        return res.fetchall()
    