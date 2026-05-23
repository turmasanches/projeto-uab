from ..database import conectar_db

class UsuarioModel:
    def __init__(self, nome, email, senha_hash, papel, id=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.papel = papel

    def salvar(self):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha_hash, papel) VALUES (?, ?, ?, ?)",
            (self.nome, self.email, self.senha_hash, self.papel)
        )
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @staticmethod
    def buscar_por_email(email):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        return row # Returning row as a dict-like object (Row) is common and matches my test expectation
