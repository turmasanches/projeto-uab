from flask import Blueprint, render_template, session, abort
from ..database import conectar_db

relatorios_bp = Blueprint('relatorios', __name__)

@relatorios_bp.route('/relatorios')
def relatorios():
    if session.get('usuario_papel') not in ('ADMIN', 'ADMIN_INICIAL', 'BIBLIOTECARIO'):
        abort(403)
        
    conn = conectar_db()
    cursor = conn.cursor()
    
    # contagem_emprestimos_periodo (simplified as total)
    cursor.execute("SELECT COUNT(*) FROM emprestimos")
    contagem_emprestimos = cursor.fetchone()[0]
    
    # top_livros
    cursor.execute('''
        SELECT l.titulo, COUNT(e.id) as total 
        FROM emprestimos e 
        JOIN livros l ON e.livro_id = l.id 
        GROUP BY l.id 
        ORDER BY total DESC LIMIT 5
    ''')
    top_livros = cursor.fetchall()
    
    # distribuicao_categorias
    cursor.execute("SELECT categoria, COUNT(*) FROM livros GROUP BY categoria")
    distribuicao_categorias = cursor.fetchall()
    
    conn.close()
    
    return render_template('relatorios.html', 
                           contagem_emprestimos=contagem_emprestimos, 
                           top_livros=top_livros, 
                           distribuicao_categorias=distribuicao_categorias)
