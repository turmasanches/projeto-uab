import pytest
from app.models.livro_model import LivroModel
from app.models.emprestimo_model import EmprestimoModel
from app.database import conectar_db

def test_solicitar_emprestimo_sucesso(client, app):
    with app.app_context():
        l = LivroModel(titulo="Livro", autor="Autor", categoria="Cat")
        l.salvar()
        v_livro_id = l.id
    
    with client.session_transaction() as sess:
        sess['usuario_papel'] = 'LEITOR'
        sess['usuario_id'] = 1
    
    response = client.post('/emprestimo/solicitar', data={'livro_id': v_livro_id})
    assert response.status_code == 302
    
    with app.app_context():
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM emprestimos WHERE livro_id = ?", (v_livro_id,))
        row = cursor.fetchone()
        assert row['status'] == 'SOLICITADO'
        conn.close()

def test_aprovar_emprestimo(client, app):
    with app.app_context():
        l = LivroModel(titulo="Livro", autor="Autor", categoria="Cat")
        l.salvar()
        v_livro_id = l.id
        e = EmprestimoModel(livro_id=v_livro_id, usuario_id=1)
        e.registrar_emprestimo()
        emp_id = e.id
    
    with client.session_transaction() as sess:
        sess['usuario_papel'] = 'BIBLIOTECARIO'
    
    response = client.post('/emprestimo/aprovar', data={'emprestimo_id': emp_id})
    assert response.status_code == 302
    
    with app.app_context():
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM emprestimos WHERE id = ?", (emp_id,))
        assert cursor.fetchone()['status'] == 'ATIVO'
        cursor.execute("SELECT status FROM livros WHERE id = ?", (v_livro_id,))
        assert cursor.fetchone()['status'] == 'EMPRESTADO'
        conn.close()

def test_devolver_emprestimo(client, app):
    with app.app_context():
        l = LivroModel(titulo="Livro", autor="Autor", categoria="Cat", status="EMPRESTADO")
        l.salvar()
        v_livro_id = l.id
        e = EmprestimoModel(livro_id=v_livro_id, usuario_id=1, status='ATIVO')
        e.registrar_emprestimo()
        emp_id = e.id
    
    with client.session_transaction() as sess:
        sess['usuario_papel'] = 'BIBLIOTECARIO'
    
    response = client.post('/emprestimo/devolver', data={'emprestimo_id': emp_id})
    assert response.status_code == 302
    
    with app.app_context():
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM emprestimos WHERE id = ?", (emp_id,))
        assert cursor.fetchone()['status'] == 'DEVOLVIDO'
        cursor.execute("SELECT status FROM livros WHERE id = ?", (v_livro_id,))
        assert cursor.fetchone()['status'] == 'DISPONIVEL'
        conn.close()
