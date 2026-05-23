from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from ..models.usuario_model import UsuarioModel

admin_bp = Blueprint('admin', __name__)

def verificar_admin():
    return session.get('usuario_papel') in ('ADMIN_INICIAL', 'ADMIN')

@admin_bp.route('/admin/dashboard')
def dashboard():
    if not verificar_admin():
        flash('Acesso negado.', 'error')
        return redirect(url_for('livros.catalogo'))
    # This could list users, etc.
    return render_template('dashboard.html')

@admin_bp.route('/admin/cadastrar-usuario', methods=['POST'])
def cadastrar_usuario():
    if not verificar_admin():
        return "Acesso Negado", 403
        
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    papel = request.form.get('papel') # 'ADMIN' or 'BIBLIOTECARIO'
    
    # Simple restriction
    if papel == 'ADMIN' and session.get('usuario_papel') != 'ADMIN_INICIAL':
        flash('Somente o Admin Inicial pode criar outros Admins.', 'error')
    else:
        if UsuarioModel.salvar(nome, email, senha, papel):
            flash(f'Usuário {papel} criado com sucesso!', 'success')
        else:
            flash('Erro ao criar usuário.', 'error')
            
    return redirect(url_for('admin.dashboard'))
