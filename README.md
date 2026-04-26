# API de Delivery com FastAPI

<p align="center">
  <img src="images/Captura de tela 2026-04-26 101517.png" width="700"/>
</p>

projeto foi desenvolvido com o objetivo de aplicar conceitos modernos de backend, incluindo:

Criação de APIs RESTful

Autenticação segura com JWT

Relacionamentos entre entidades

Boas práticas de arquitetura

A API permite gerenciar:

Usuários, 
 Pedidos,
 Itens de pedidos,
 Controle de acesso.
# Tecnologias utilizadas

Python

FastAPI

SQLAlchemy (ORM)

Banco de dados (SQLite / PostgreSQL)

Uvicorn

Pydantic

Alembic (migrações)


O FastAPI foi escolhido por oferecer:

✔ Alta performance (baseado em async)
✔ Sintaxe moderna com type hints
✔ Validação automática com Pydantic
✔ Documentação automática (Swagger e Redoc)
✔ Suporte nativo a async/await

# Funcionalidades principais

Cadastro e autenticação de usuários (JWT)

Refresh Token

Controle de acesso por níveis

CRUD de pedidos

Relacionamento entre tabelas

Validação de dados automática

Documentação interativa da API


# Como executar o projeto
Clone o repositório:
git clone "https://github.com/seu-usuario/seu-projeto.git"

Acesse a pasta: cd seu-projeto

Crie o ambiente virtual: python -m venv venv

Ative o ambiente: venv\Scripts\activate

Instale as dependências: pip install -r requirements.txt

Execute a API: uvicorn app.main:app --reload



# Neste projeto foram aplicados conceitos importantes como:

Arquitetura de APIs profissionais

Autenticação com JWT e Refresh Token

Modelagem de banco de dados

Relacionamentos com SQLAlchemy

Otimização de consultas (Lazy Loading)

Padronização com Schemas


Este projeto simula um sistema real de backend, sendo ideal para demonstrar habilidades em: Desenvolvimento backend com Python
, Construção de APIs escaláveis
, Segurança e autenticação
, Boas práticas de código
