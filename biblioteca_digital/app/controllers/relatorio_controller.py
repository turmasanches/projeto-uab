from flask import Blueprint, render_template, session, flash, redirect, url_for
from ..database import conectar_db

relatorios_bp = Blueprint('relatorios', __name__)

@relatorios_bp.route('/relatorios')
def relatorios():
    if session.get('usuario_papel') not in ('ADMIN', 'ADMIN_INICIAL', 'BIBLIOTECARIO'):
        flash('Acesso negado.', 'error')
        return redirect(url_for('livros.catalogo'))
        
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Metrics
    cursor.execute("SELECT COUNT(*) FROM emprestimos WHERE status = 'ATIVO'")
    ativos = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM livros")
    total_livros = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT l.titulo, COUNT(e.id) as total 
        FROM emprestimos e 
        JOIN livros l ON e.livro_id = l.id 
        GROUP BY e.livro_id 
        ORDER BY total DESC LIMIT 5
    ''')
    top_livros = cursor.fetchall()
    
    conn.close()
    
    return render_template('relatorios.html', ativos=ativos, total_livros=total_livros, top_livros=top_livros)
