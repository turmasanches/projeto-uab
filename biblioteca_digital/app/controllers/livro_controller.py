from flask import Blueprint, request, render_template, redirect, url_for, session, abort
from ..models.livro_model import LivroModel

livros_bp = Blueprint('livros', __name__)

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
    if session.get('usuario_papel') not in ('BIBLIOTECARIO', 'ADMIN', 'ADMIN_INICIAL'):
        abort(403)
        
    titulo = request.form.get('titulo')
    autor = request.form.get('autor')
    categoria = request.form.get('categoria')
    
    livro = LivroModel(titulo=titulo, autor=autor, categoria=categoria)
    livro.salvar()
    return redirect(url_for('livros.catalogo'))
