# Use uma imagem leve do Python
FROM python:3.11-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Instalando dependências de sistema
RUN apt-get update && apt-get install -y mariadb-client libmariadb-dev libmariadb3 gcc curl

# Copie o arquivo de requisitos e instale as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação para dentro do contêiner
COPY . ./src
COPY alembic.ini alembic.ini

# Exponha a porta usada pela aplicação
EXPOSE 8000

ENV PYTHONPATH="/app"

# Adiciona script auxiliar para esperar o banco ser executado
RUN curl -o wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh
RUN chmod +x wait-for-it.sh

# Comando para rodar o servidor com hot reload
CMD ["alembic", "upgrade", "head", "&&", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
