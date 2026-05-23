from ..database import conectar_db

class LivroModel:
    def __init__(self, titulo, autor, categoria, status='DISPONIVEL', id=None):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.status = status

    def salvar(self):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO livros (titulo, autor, categoria, status) VALUES (?, ?, ?, ?)",
            (self.titulo, self.autor, self.categoria, self.status)
        )
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @staticmethod
    def buscar_todos(filtros=None):
        conn = conectar_db()
        cursor = conn.cursor()
        query = "SELECT * FROM livros"
        params = []
        if filtros:
            conditions = []
            if 'titulo' in filtros:
                conditions.append("titulo LIKE ?")
                params.append(f"%{filtros['titulo']}%")
            if 'autor' in filtros:
                conditions.append("autor LIKE ?")
                params.append(f"%{filtros['autor']}%")
            if 'categoria' in filtros:
                conditions.append("categoria LIKE ?")
                params.append(f"%{filtros['categoria']}%")
            if conditions:
                query += " WHERE " + " OR ".join(conditions) # markdow.md says "titulo, autor OU categoria"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def atualizar_status(id, novo_status):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE livros SET status = ? WHERE id = ?", (novo_status, id))
        conn.commit()
        conn.close()
