# Sistema de Biblioteca Digital

Este é um sistema de gerenciamento de biblioteca digital desenvolvido com Flask e SQLite.

## Requisitos

- Python 3.10+
- Flask 3.0.0
- SQLite 3
- Docker (opcional)

## Estrutura do Projeto

- `app/`: Contém o código fonte da aplicação.
  - `controllers/`: Gerenciam as rotas e a lógica de negócio.
  - `models/`: Definem a estrutura dos dados e interações com o banco de dados.
  - `templates/`: Arquivos HTML (Jinja2) com Tailwind CSS.
  - `database.py`: Gerenciamento da conexão e inicialização do banco de dados.
- `config.py`: Configurações da aplicação.
- `run.py`: Ponto de entrada para execução do servidor.
- `.env`: Variáveis de ambiente (criado a partir de `.env.example`).

## Como Executar

### Usando Docker (Recomendado)

1. Construa a imagem:
   ```bash
   docker build -t biblioteca_digital .
   ```

2. Execute o container:
   ```bash
   docker run -p 5000:5000 biblioteca_digital
   ```

### Execução Local

1. Crie um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente:
   ```bash
   cp .env.example .env
   # Edite o arquivo .env se necessário
   ```

4. Execute a aplicação:
   ```bash
   python3 run.py
   ```

A aplicação estará disponível em `http://localhost:5000`.

## Usuário Inicial

O sistema é inicializado com um usuário administrador padrão definido no arquivo `.env`:
- **E-mail:** admin@empresa.com
- **Senha:** senha_segura
