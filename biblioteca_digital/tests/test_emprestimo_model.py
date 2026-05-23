import pytest
from app.models.emprestimo_model import EmprestimoModel
from app.models.livro_model import LivroModel
from app.models.usuario_model import UsuarioModel

def test_registrar_e_finalizar_emprestimo(db):
    # Setup dependents
    usuario = UsuarioModel(nome="User", email="user@email.com", senha_hash="hash", papel="LEITOR")
    usuario.salvar()
    livro = LivroModel(titulo="Livro", autor="Autor", categoria="Cat")
    livro.salvar()
    
    emprestimo = EmprestimoModel(livro_id=livro.id, usuario_id=usuario.id)
    emprestimo.registrar_emprestimo()
    
    assert emprestimo.id is not None
    
    # Finalize
    EmprestimoModel.finalizar_emprestimo(emprestimo.id)
    
    # Check status
    conn = db
    cursor = conn.cursor()
    cursor.execute("SELECT status, data_devolucao FROM emprestimos WHERE id = ?", (emprestimo.id,))
    row = cursor.fetchone()
    assert row['status'] == "DEVOLVIDO"
    assert row['data_devolucao'] is not None
