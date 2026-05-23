# Plano de Testes - Sistema de Biblioteca Digital

Este documento descreve a estratégia de testes automatizados para o Sistema de Biblioteca Digital, seguindo a metodologia **TDD (Test-Driven Development) First**. O objetivo é garantir a integridade das funcionalidades críticas, evitar regressões e assegurar que as regras de negócio sejam respeitadas.

## 1. Estratégia de Testes

### 1.1 Metodologia
Será adotada a prática de TDD, onde os testes são escritos antes da implementação da funcionalidade ou durante a refatoração.
- **Red**: Criar um teste que falha para uma nova funcionalidade.
- **Green**: Implementar o código mínimo necessário para o teste passar.
- **Refactor**: Melhorar o código mantendo os testes passando.

### 1.2 Ferramentas
- **Framework**: `pytest`
- **Extensões**: 
  - `pytest-flask`: Integração com o ciclo de vida do Flask.
  - `pytest-mock`: Para substituição de dependências (mocks).
  - `pytest-cov`: Para medição de cobertura de código.
- **Banco de Dados**: SQLite em memória (`:memory:`) para garantir isolamento e velocidade.

---

## 2. Cenários de Teste por Funcionalidade

### 2.1 Autenticação e Usuários (`auth_controller.py`)
| ID | Cenário | Descrição | Prioridade |
|:---|:---|:---|:---|
| CT-AUTH-01 | Login com Sucesso | Validar se um usuário cadastrado consegue logar com credenciais válidas. | Crítica |
| CT-AUTH-02 | Login com Falha | Garantir que credenciais inválidas (email ou senha) não permitam acesso. | Crítica |
| CT-AUTH-03 | Cadastro de Leitor | Validar se um novo leitor pode se autocadastrar e se o papel atribuído é 'LEITOR'. | Alta |
| CT-AUTH-04 | Logout | Verificar se a sessão é limpa corretamente após o logout. | Média |

### 2.2 Gestão Administrativa (`admin_controller.py`)
| ID | Cenário | Descrição | Prioridade |
|:---|:---|:---|:---|
| CT-ADM-01 | Criar Admin (ADMIN_INICIAL) | Apenas o `ADMIN_INICIAL` pode criar novos usuários do tipo `ADMIN`. | Crítica |
| CT-ADM-02 | Criar Bibliotecário | `ADMIN_INICIAL` ou `ADMIN` podem criar usuários do tipo `BIBLIOTECARIO`. | Alta |
| CT-ADM-03 | Bloqueio de Acesso | Garantir que um `LEITOR` ou `BIBLIOTECARIO` não consiga criar administradores. | Crítica |

### 2.3 Gestão de Livros (`livro_controller.py`)
| ID | Cenário | Descrição | Prioridade |
|:---|:---|:---|:---|
| CT-LIV-01 | Cadastro de Livro | Validar cadastro por `BIBLIOTECARIO` ou `ADMIN`. | Alta |
| CT-LIV-02 | Busca no Catálogo | Verificar filtros por título, autor ou categoria. | Média |
| CT-LIV-03 | Permissão Negada | Garantir que `LEITOR` não consiga cadastrar livros. | Crítica |

### 2.4 Fluxo de Empréstimos (`emprestimo_controller.py`)
| ID | Cenário | Descrição | Prioridade |
|:---|:---|:---|:---|
| CT-EMP-01 | Solicitação de Empréstimo | `LEITOR` solicita livro `DISPONIVEL`. Status deve mudar para `SOLICITADO`. | Crítica |
| CT-EMP-02 | Aprovação de Empréstimo | `BIBLIOTECARIO` aprova. Status do livro vai para `EMPRESTADO` e empréstimo para `ATIVO`. | Crítica |
| CT-EMP-03 | Devolução de Livro | `BIBLIOTECARIO` registra devolução. Livro volta a ficar `DISPONIVEL`. | Crítica |
| CT-EMP-04 | Impedir Duplo Empréstimo | Garantir que livro `EMPRESTADO` não possa ser solicitado novamente. | Crítica |

### 2.5 Relatórios e Métricas (`relatorio_controller.py`)
| ID | Cenário | Descrição | Prioridade |
|:---|:---|:---|:---|
| CT-REL-01 | Acesso a Relatórios | Validar que apenas `ADMIN` ou `BIBLIOTECARIO` acessam a página. | Alta |
| CT-REL-02 | Consistência de Dados | Verificar se as contagens (top livros, total empréstimos) condizem com o DB. | Média |

---

## 3. Implementação Técnica

### 3.1 Fixtures Base (`conftest.py`)
Os testes utilizarão uma fixture para configurar o app em modo de teste e inicializar o banco de dados em memória antes de cada execução.

```python
@pytest.fixture
def app():
    os.environ['DATABASE_PATH'] = ':memory:'
    app = criar_app()
    return app

@pytest.fixture
def client(app):
    return app.test_client()
```

### 3.2 Uso de Mocks
Mocks serão utilizados para:
- Simular o envio de e-mails (se implementado futuramente).
- Simular erros de conexão com banco de dados para testar resiliência.
- Simular tempo (dates/timestamps) em testes de expiração de empréstimo.

---

## 4. Manutenção e Regressão

1. **Execução Local**: Todos os desenvolvedores devem rodar `pytest` antes de realizar commits.
2. **Cobertura Mínima**: Recomenda-se uma cobertura mínima de **80%** de linhas de código.
3. **Falhas em CI**: Qualquer falha nos testes automatizados deve impedir o merge/deploy da alteração.
