import pytest
from app.models.usuario_model import UsuarioModel

def test_criar_usuario(db):
    usuario = UsuarioModel(nome="Teste", email="teste@email.com", senha_hash="hash", papel="LEITOR")
    usuario.salvar()
    
    buscado = UsuarioModel.buscar_por_email("teste@email.com")
    assert buscado is not None
    assert buscado['nome'] == "Teste"
    assert buscado['papel'] == "LEITOR"

def test_buscar_usuario_inexistente(db):
    buscado = UsuarioModel.buscar_por_email("naoexiste@email.com")
    assert buscado is None
