from ..database import conectar_db

class LivroModel:
    def __init__(self, id=None, titulo=None, autor=None, categoria=None, status='DISPONIVEL'):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.status = status

    @staticmethod
    def salvar(titulo, autor, categoria):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO livros (titulo, autor, categoria) VALUES (?, ?, ?)",
            (titulo, autor, categoria)
        )
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
                query += " WHERE " + " AND ".join(conditions)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [LivroModel(row['id'], row['titulo'], row['autor'], row['categoria'], row['status']) for row in rows]

    @staticmethod
    def buscar_por_id(id):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM livros WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return LivroModel(row['id'], row['titulo'], row['autor'], row['categoria'], row['status'])
        return None

    @staticmethod
    def atualizar_status(id, novo_status):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE livros SET status = ? WHERE id = ?", (novo_status, id))
        conn.commit()
        conn.close()
