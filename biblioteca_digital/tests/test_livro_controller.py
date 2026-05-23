import pytest
from app.models.livro_model import LivroModel

def test_catalogo_busca(client, app):
    with app.app_context():
        LivroModel(titulo="Busca Teste", autor="Autor", categoria="Cat").salvar()
    
    response = client.get('/catalogo?titulo=Busca')
    assert response.status_code == 200
    # Check if results are in the rendered template (we can check data)
    assert b'Busca Teste' in response.data

def test_cadastrar_livro_sucesso(client, app):
    with client.session_transaction() as sess:
        sess['usuario_papel'] = 'BIBLIOTECARIO'
    
    response = client.post('/livro/cadastrar', data={
        'titulo': 'Novo Livro',
        'autor': 'Novo Autor',
        'categoria': 'Nova Cat'
    })
    assert response.status_code == 302 # Assuming redirect after save
    
    with app.app_context():
        livros = LivroModel.buscar_todos({'titulo': 'Novo Livro'})
        assert len(livros) == 1

def test_cadastrar_livro_negado(client, app):
    with client.session_transaction() as sess:
        sess['usuario_papel'] = 'LEITOR'
    
    response = client.post('/livro/cadastrar', data={
        'titulo': 'Livro Proibido',
        'autor': 'Autor',
        'categoria': 'Cat'
    })
    assert response.status_code == 403
    
    with app.app_context():
        livros = LivroModel.buscar_todos({'titulo': 'Livro Proibido'})
        assert len(livros) == 0
