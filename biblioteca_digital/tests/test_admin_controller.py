import pytest
from app.models.usuario_model import UsuarioModel

def test_cadastrar_admin_sucesso(client, app):
    # Setup ADMIN_INICIAL session
    with client.session_transaction() as sess:
        sess['usuario_papel'] = 'ADMIN_INICIAL'
    
    response = client.post('/admin/cadastrar-admin', data={
        'nome': 'Admin 1',
        'email': 'admin1@email.com',
        'senha': 'password'
    })
    assert response.status_code == 302 # Redirect
    
    with app.app_context():
        u = UsuarioModel.buscar_por_email('admin1@email.com')
        assert u is not None
        assert u['papel'] == 'ADMIN'

def test_cadastrar_admin_bloqueio(client, app):
    # Setup LEITOR session
    with client.session_transaction() as sess:
        sess['usuario_papel'] = 'LEITOR'
    
    response = client.post('/admin/cadastrar-admin', data={
        'nome': 'Hacker',
        'email': 'hacker@email.com',
        'senha': 'password'
    })
    # Should block access, maybe 403 or redirect
    assert response.status_code in [403, 302]
    
    with app.app_context():
        u = UsuarioModel.buscar_por_email('hacker@email.com')
        assert u is None

def test_cadastrar_bibliotecario_por_admin(client, app):
    with client.session_transaction() as sess:
        sess['usuario_papel'] = 'ADMIN'
    
    response = client.post('/admin/cadastrar-bibliotecario', data={
        'nome': 'Biblio 1',
        'email': 'bib1@email.com',
        'senha': 'password'
    })
    assert response.status_code == 302
    
    with app.app_context():
        u = UsuarioModel.buscar_por_email('bib1@email.com')
        assert u is not None
        assert u['papel'] == 'BIBLIOTECARIO'
