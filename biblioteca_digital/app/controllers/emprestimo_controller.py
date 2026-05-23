from flask import Blueprint, request, redirect, url_for, session, flash, render_template
from ..models.emprestimo_model import EmprestimoModel
from ..models.livro_model import LivroModel

emprestimos_bp = Blueprint('emprestimos', __name__)

@emprestimos_bp.route('/emprestimo/solicitar/<int:livro_id>', methods=['POST'])
def solicitar(livro_id):
    if not session.get('usuario_id'):
        flash('Faça login para solicitar um livro.', 'warning')
        return redirect(url_for('auth.login'))
        
    livro = LivroModel.buscar_por_id(livro_id)
    if livro and livro.status == 'DISPONIVEL':
        EmprestimoModel.registrar_emprestimo(livro_id, session['usuario_id'])
        flash('Solicitação enviada!', 'success')
    else:
        flash('Livro indisponível.', 'error')
        
    return redirect(url_for('livros.catalogo'))

@emprestimos_bp.route('/admin/emprestimos')
def gerenciar():
    if session.get('usuario_papel') not in ('ADMIN', 'ADMIN_INICIAL', 'BIBLIOTECARIO'):
        flash('Acesso negado.', 'error')
        return redirect(url_for('livros.catalogo'))
        
    emprestimos = EmprestimoModel.buscar_todos()
    return render_template('emprestimos.html', emprestimos=emprestimos)

@emprestimos_bp.route('/emprestimo/aprovar/<int:id>', methods=['POST'])
def aprovar(id):
    if session.get('usuario_papel') not in ('ADMIN', 'ADMIN_INICIAL', 'BIBLIOTECARIO'):
        return "Acesso Negado", 403
        
    emprestimo = EmprestimoModel.buscar_por_id(id)
    if emprestimo:
        EmprestimoModel.atualizar_status(id, 'ATIVO')
        LivroModel.atualizar_status(emprestimo.livro_id, 'EMPRESTADO')
        flash('Empréstimo aprovado!', 'success')
        
    return redirect(url_for('emprestimos.gerenciar'))

@emprestimos_bp.route('/emprestimo/devolver/<int:id>', methods=['POST'])
def devolver(id):
    if session.get('usuario_papel') not in ('ADMIN', 'ADMIN_INICIAL', 'BIBLIOTECARIO'):
        return "Acesso Negado", 403
        
    emprestimo = EmprestimoModel.buscar_por_id(id)
    if emprestimo:
        EmprestimoModel.atualizar_status(id, 'DEVOLVIDO')
        LivroModel.atualizar_status(emprestimo.livro_id, 'DISPONIVEL')
        flash('Livro devolvido!', 'success')
        
    return redirect(url_for('emprestimos.gerenciar'))
