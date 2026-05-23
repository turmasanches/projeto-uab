from ..database import conectar_db
from datetime import datetime

class EmprestimoModel:
    def __init__(self, livro_id, usuario_id, status='SOLICITADO', data_solicitacao=None, data_devolucao=None, id=None):
        self.id = id
        self.livro_id = livro_id
        self.usuario_id = usuario_id
        self.status = status
        self.data_solicitacao = data_solicitacao
        self.data_devolucao = data_devolucao

    def registrar_emprestimo(self):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO emprestimos (livro_id, usuario_id, status) VALUES (?, ?, ?)",
            (self.livro_id, self.usuario_id, self.status)
        )
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @staticmethod
    def finalizar_emprestimo(id):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE emprestimos SET status = 'DEVOLVIDO', data_devolucao = ? WHERE id = ?",
            (datetime.now(), id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def atualizar_status(id, novo_status):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE emprestimos SET status = ? WHERE id = ?", (novo_status, id))
        conn.commit()
        conn.close()
