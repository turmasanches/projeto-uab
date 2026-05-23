from ..database import conectar_db
from datetime import datetime

class EmprestimoModel:
    def __init__(self, id=None, livro_id=None, usuario_id=None, data_solicitacao=None, data_devolucao=None, status='SOLICITADO'):
        self.id = id
        self.livro_id = livro_id
        self.usuario_id = usuario_id
        self.data_solicitacao = data_solicitacao
        self.data_devolucao = data_devolucao
        self.status = status

    @staticmethod
    def registrar_emprestimo(livro_id, usuario_id):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO emprestimos (livro_id, usuario_id, status) VALUES (?, ?, 'SOLICITADO')",
            (livro_id, usuario_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def buscar_por_id(id):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM emprestimos WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return EmprestimoModel(row['id'], row['livro_id'], row['usuario_id'], row['data_solicitacao'], row['data_devolucao'], row['status'])
        return None

    @staticmethod
    def buscar_todos():
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT e.*, l.titulo as livro_titulo, u.nome as usuario_nome 
            FROM emprestimos e
            JOIN livros l ON e.livro_id = l.id
            JOIN usuarios u ON e.usuario_id = u.id
        ''')
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def atualizar_status(id, novo_status):
        conn = conectar_db()
        cursor = conn.cursor()
        if novo_status == 'DEVOLVIDO':
            cursor.execute(
                "UPDATE emprestimos SET status = ?, data_devolucao = ? WHERE id = ?",
                (novo_status, datetime.now(), id)
            )
        else:
            cursor.execute("UPDATE emprestimos SET status = ? WHERE id = ?", (novo_status, id))
        conn.commit()
        conn.close()
