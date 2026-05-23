from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from ..models.usuario_model import UsuarioModel

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        usuario = UsuarioModel.buscar_por_email(email)
        
        if usuario and usuario.verificar_senha(senha):
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            session['usuario_papel'] = usuario.papel
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('livros.catalogo'))
        else:
            flash('E-mail ou senha inválidos.', 'error')
            
    return render_template('login.html')

@auth_bp.route('/cadastrar-leitor', methods=['GET', 'POST'])
def cadastrar_leitor():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        if UsuarioModel.salvar(nome, email, senha, 'LEITOR'):
            flash('Cadastro realizado! Faça login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Erro ao cadastrar. E-mail já existe?', 'error')
            
    return render_template('cadastro.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth.login'))
