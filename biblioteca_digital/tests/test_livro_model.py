import pytest
from app.models.livro_model import LivroModel

def test_criar_e_buscar_livro(db):
    livro = LivroModel(titulo="Dom Casmurro", autor="Machado de Assis", categoria="Literatura")
    livro.salvar()
    
    livros = LivroModel.buscar_todos({"titulo": "Dom Casmurro"})
    assert len(livros) == 1
    assert livros[0]['titulo'] == "Dom Casmurro"
    assert livros[0]['status'] == "DISPONIVEL"

def test_atualizar_status_livro(db):
    livro = LivroModel(titulo="O Cortiço", autor="Aluísio Azevedo", categoria="Literatura")
    livro.salvar()
    
    LivroModel.atualizar_status(livro.id, "EMPRESTADO")
    
    livros = LivroModel.buscar_todos({"titulo": "O Cortiço"})
    assert livros[0]['status'] == "EMPRESTADO"

def test_buscar_por_autor(db):
    LivroModel(titulo="Livro 1", autor="Autor A", categoria="Cat 1").salvar()
    LivroModel(titulo="Livro 2", autor="Autor B", categoria="Cat 2").salvar()
    
    livros = LivroModel.buscar_todos({"autor": "Autor A"})
    assert len(livros) == 1
    assert livros[0]['autor'] == "Autor A"
