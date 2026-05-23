from flask import Blueprint, request, redirect, url_for, session, abort
from ..models.usuario_model import UsuarioModel
from werkzeug.security import generate_password_hash

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/cadastrar-admin', methods=['POST'])
def cadastrar_admin():
    if session.get('usuario_papel') != 'ADMIN_INICIAL':
        abort(403)
    
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    
    senha_hash = generate_password_hash(senha)
    usuario = UsuarioModel(nome=nome, email=email, senha_hash=senha_hash, papel='ADMIN')
    usuario.salvar()
    return redirect(url_for('auth.dashboard'))

@admin_bp.route('/admin/cadastrar-bibliotecario', methods=['POST'])
def cadastrar_bibliotecario():
    if session.get('usuario_papel') not in ('ADMIN_INICIAL', 'ADMIN'):
        abort(403)
        
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    
    senha_hash = generate_password_hash(senha)
    usuario = UsuarioModel(nome=nome, email=email, senha_hash=senha_hash, papel='BIBLIOTECARIO')
    usuario.salvar()
    return redirect(url_for('auth.dashboard'))
