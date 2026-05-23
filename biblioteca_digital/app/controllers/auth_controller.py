from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from ..models.usuario_model import UsuarioModel
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        usuario = UsuarioModel.buscar_por_email(email)
        
        if usuario and check_password_hash(usuario['senha_hash'], senha):
            session['usuario_id'] = usuario['id']
            session['usuario_nome'] = usuario['nome']
            session['usuario_papel'] = usuario['papel']
            return redirect(url_for('auth.dashboard')) # 'REDIRECIONAR painel'
        
    return render_template('login.html')

@auth_bp.route('/cadastrar-leitor', methods=['GET', 'POST'])
def cadastrar_leitor():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        senha_hash = generate_password_hash(senha)
        usuario = UsuarioModel(nome=nome, email=email, senha_hash=senha_hash, papel='LEITOR')
        usuario.salvar()
        return redirect(url_for('auth.login'))
            
    return render_template('cadastro.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
