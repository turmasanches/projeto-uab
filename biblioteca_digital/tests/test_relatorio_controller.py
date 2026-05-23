import pytest

def test_acesso_relatorios_sucesso(client, app):
    with client.session_transaction() as sess:
        sess['usuario_papel'] = 'ADMIN'
    
    response = client.get('/relatorios')
    assert response.status_code == 200

def test_acesso_relatorios_negado(client, app):
    with client.session_transaction() as sess:
        sess['usuario_papel'] = 'LEITOR'
    
    response = client.get('/relatorios')
    assert response.status_code == 403
