import pytest
from flask import session
from app.models.usuario_model import UsuarioModel
from werkzeug.security import generate_password_hash

def test_login_sucesso(client, app):
    with app.app_context():
        senha_hash = generate_password_hash("senha123")
        usuario = UsuarioModel(nome="Teste", email="teste@email.com", senha_hash=senha_hash, papel="LEITOR")
        usuario.salvar()
    
    response = client.post('/login', data={'email': 'teste@email.com', 'senha': 'senha123'}, follow_redirects=True)
    assert response.status_code == 200
    # Assuming redirect to dashboard as per pseudocode "REDIRECIONAR painel"
    # I'll check if session has user info
    with client.session_transaction() as sess:
        assert sess.get('usuario_id') is not None

def test_login_falha(client, app):
    response = client.post('/login', data={'email': 'errado@email.com', 'senha': 'senha'}, follow_redirects=True)
    assert response.status_code == 200 # Usually re-renders login page
    with client.session_transaction() as sess:
        assert sess.get('usuario_id') is None

def test_cadastrar_leitor(client, app):
    response = client.post('/cadastrar-leitor', data={
        'nome': 'Novo Leitor',
        'email': 'novo@email.com',
        'senha': 'password'
    }, follow_redirects=True)
    assert response.status_code == 200
    
    with app.app_context():
        usuario = UsuarioModel.buscar_por_email('novo@email.com')
        assert usuario is not None
        assert usuario['papel'] == 'LEITOR'

def test_logout(client, app):
    with client.session_transaction() as sess:
        sess['usuario_id'] = 1
    
    response = client.get('/logout', follow_redirects=True)
    with client.session_transaction() as sess:
        assert sess.get('usuario_id') is None
