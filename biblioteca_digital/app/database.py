import sqlite3
import os
from werkzeug.security import generate_password_hash
from config import Config

def conectar_db():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def inicializar_db():
    # Ensure directory exists
    os.makedirs(os.path.dirname(Config.DATABASE_PATH), exist_ok=True)
    
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Create Tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL,
            papel TEXT NOT NULL -- 'ADMIN_INICIAL', 'ADMIN', 'BIBLIOTECARIO', 'LEITOR'
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            categoria TEXT NOT NULL,
            status TEXT DEFAULT 'DISPONIVEL' -- 'DISPONIVEL', 'EMPRESTADO'
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            livro_id INTEGER NOT NULL,
            usuario_id INTEGER NOT NULL,
            data_solicitacao DATETIME DEFAULT CURRENT_TIMESTAMP,
            data_devolucao DATETIME,
            status TEXT DEFAULT 'SOLICITADO', -- 'SOLICITADO', 'ATIVO', 'DEVOLVIDO'
            FOREIGN KEY (livro_id) REFERENCES livros (id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    ''')
    
    # Initial Admin Setup
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        senha_hash = generate_password_hash(Config.PROPRIETARIO_PASSWORD)
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha_hash, papel) VALUES (?, ?, ?, ?)",
            ("Admin Inicial", Config.PROPRIETARIO_EMAIL, senha_hash, 'ADMIN_INICIAL')
        )
    
    conn.commit()
    conn.close()
