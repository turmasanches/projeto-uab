from ..database import conectar_db
from werkzeug.security import generate_password_hash, check_password_hash

class UsuarioModel:
    def __init__(self, id=None, nome=None, email=None, senha_hash=None, papel=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.papel = papel

    @staticmethod
    def salvar(nome, email, senha, papel):
        conn = conectar_db()
        cursor = conn.cursor()
        senha_hash = generate_password_hash(senha)
        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha_hash, papel) VALUES (?, ?, ?, ?)",
                (nome, email, senha_hash, papel)
            )
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()

    @staticmethod
    def buscar_por_email(email):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return UsuarioModel(row['id'], row['nome'], row['email'], row['senha_hash'], row['papel'])
        return None

    @staticmethod
    def buscar_por_id(id):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return UsuarioModel(row['id'], row['nome'], row['email'], row['senha_hash'], row['papel'])
        return None

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)
