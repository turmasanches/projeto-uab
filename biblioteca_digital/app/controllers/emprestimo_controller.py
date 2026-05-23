from flask import Blueprint, request, redirect, url_for, session, abort
from ..models.emprestimo_model import EmprestimoModel
from ..models.livro_model import LivroModel
from ..database import conectar_db

emprestimos_bp = Blueprint('emprestimos', __name__)

@emprestimos_bp.route('/admin/emprestimos')
def gerenciar():
    if session.get('usuario_papel') not in ('ADMIN', 'ADMIN_INICIAL', 'BIBLIOTECARIO'):
        abort(403)
        
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT e.*, l.titulo as livro_titulo, u.nome as usuario_nome 
        FROM emprestimos e
        JOIN livros l ON e.livro_id = l.id
        JOIN usuarios u ON e.usuario_id = u.id
    ''')
    emprestimos = cursor.fetchall()
    conn.close()
    return render_template('emprestimos.html', emprestimos=emprestimos)

@emprestimos_bp.route('/emprestimo/solicitar', methods=['POST'])
def solicitar():
    if session.get('usuario_papel') != 'LEITOR':
        abort(403)
    
    livro_id = request.form.get('livro_id')
    
    # Check if book is available
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM livros WHERE id = ?", (livro_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row and row['status'] == 'DISPONIVEL':
        emprestimo = EmprestimoModel(livro_id=livro_id, usuario_id=session.get('usuario_id'))
        emprestimo.registrar_emprestimo()
    
    return redirect(url_for('livros.catalogo'))

@emprestimos_bp.route('/emprestimo/aprovar', methods=['POST'])
def aprovar():
    if session.get('usuario_papel') != 'BIBLIOTECARIO':
        abort(403)
        
    emprestimo_id = request.form.get('emprestimo_id')
    
    # Get livro_id from emprestimo
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT livro_id FROM emprestimos WHERE id = ?", (emprestimo_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        livro_id = row['livro_id']
        EmprestimoModel.atualizar_status(emprestimo_id, 'ATIVO')
        LivroModel.atualizar_status(livro_id, 'EMPRESTADO')
        # GERAR log (omitted as per simplicity if not specified)
        
    return redirect(url_for('auth.dashboard'))

@emprestimos_bp.route('/emprestimo/devolver', methods=['POST'])
def devolver():
    if session.get('usuario_papel') != 'BIBLIOTECARIO':
        abort(403)
        
    emprestimo_id = request.form.get('emprestimo_id')
    
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT livro_id FROM emprestimos WHERE id = ?", (emprestimo_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        livro_id = row['livro_id']
        EmprestimoModel.finalizar_emprestimo(emprestimo_id)
        LivroModel.atualizar_status(livro_id, 'DISPONIVEL')
        
    return redirect(url_for('auth.dashboard'))
