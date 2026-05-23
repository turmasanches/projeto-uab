from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from ..models.livro_model import LivroModel

livros_bp = Blueprint('livros', __name__)

@livros_bp.route('/')
@livros_bp.route('/catalogo')
def catalogo():
    filtros = {}
    if request.args.get('titulo'): filtros['titulo'] = request.args.get('titulo')
    if request.args.get('autor'): filtros['autor'] = request.args.get('autor')
    if request.args.get('categoria'): filtros['categoria'] = request.args.get('categoria')
    
    livros = LivroModel.buscar_todos(filtros)
    return render_template('catalogo.html', livros=livros)

@livros_bp.route('/livro/cadastrar', methods=['POST'])
def cadastrar():
    if session.get('usuario_papel') not in ('ADMIN', 'ADMIN_INICIAL', 'BIBLIOTECARIO'):
        flash('Sem permissão para cadastrar livros.', 'error')
        return redirect(url_for('livros.catalogo'))
        
    titulo = request.form.get('titulo')
    autor = request.form.get('autor')
    categoria = request.form.get('categoria')
    
    LivroModel.salvar(titulo, autor, categoria)
    flash('Livro cadastrado com sucesso!', 'success')
    return redirect(url_for('livros.catalogo'))
