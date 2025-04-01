# Sistema Higor e Rafael

Este sistema foi desenvolvido como um estudo da **FastAPI** e como parte do treinamento pessoal de Rafael.  
O repositório faz parte de um projeto no qual foi decidido que Rafael ficaria responsável pelo backend, desde a estruturação até o desenvolvimento, seguindo boas práticas e padronizações.

As decisões sobre tecnologias e frameworks foram tomadas em conjunto por **Higor e Rafael**, levando em consideração afinidade e melhor adequação para o projeto.  

O objetivo inicial do sistema é desenvolver um **MVP de um sistema ERP para lojas com produtos**, utilizando **TDD** (Test-Driven Development) para garantir qualidade e escalabilidade do código.  

Além disso, o projeto busca fornecer uma **arquitetura bem estruturada**, adequada para sistemas de **médio/grande porte**, servindo como molde para projetos futuros.  

> 📝 **Padronização:**  
> As classes e nomes das entidades foram padronizadas em **português** para facilitar a compreensão de novos desenvolvedores que ingressarem no projeto.

---

## **🚀 Tecnologias Utilizadas**
Este projeto foi desenvolvido utilizando as seguintes tecnologias:

- [FastAPI](https://fastapi.tiangolo.com/) – Framework web para APIs rápidas e eficientes.
- [SQLAlchemy](https://www.sqlalchemy.org/) – ORM para manipulação do banco de dados.
- [Pydantic](https://pydantic-docs.helpmanual.io/) – Validação de dados e schemas.
- [Docker](https://www.docker.com/) – Virtualização do ambiente.
- [Alembic](https://alembic.sqlalchemy.org/) – Controle de versões do banco de dados.
- [Pytest](https://pytest.org/) – Testes unitários e de integração.

---

## **🛠️ Como Rodar o Projeto**

### **🔹 Pré-requisitos**
Antes de começar, você precisa ter instalado:
- Python 3.11.9
- Docker e Docker Compose (opcional)
- MariaDB (caso não utilize Docker)

## Estrutura do Projeto

Na pasta `src/` estão todos os arquivos principais do sistema. A estrutura é organizada da seguinte forma:

- **`api/`** – Contém as rotas da aplicação. Aqui são definidos os endpoints, além do tratamento de acessos e erros.
- **`core/`** – Arquivos essenciais do sistema, como logs, manipulação de erros personalizados, segurança e outras configurações reutilizáveis.
- **`db/`** – Contém arquivos relacionados ao banco de dados, incluindo migrações e modelos (`models`).
- **`repositories/`** – Camada responsável pelas operações no banco de dados, contendo a lógica de acesso e manipulação das informações armazenadas.
- **`schemas/`** – Define as classes de validação das entradas e saídas das requisições, utilizando Pydantic.
- **`services/`** – Onde se encontra a lógica de negócio do sistema, separando regras específicas da aplicação.
- **`tests/`** – Contém os testes unitários e de integração para garantir a confiabilidade do sistema.
- **`utils/`** – Armazena funções auxiliares, como envio de e-mails e integração com serviços de terceiros.

Além disso, temos:
- **`logs/`** – Diretório onde os arquivos de log são armazenados.
- **`uploads/`** – Diretório para armazenar arquivos enviados pelo sistema.
- **`.docker/`** – Volume do banco de dados, utilizado para garantir a persistência dos dados no ambiente Docker.
- **`.venv/`** – Contém o ambiente virtual e as bibliotecas necessárias para o sistema.

## Exemplo de uma migration
Como gerar migration
``` bash
alembic revision --autogenerate -m "Initial models"
alembic upgrade head
```
