FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Instalar o utilitário pg_isready para verificar a disponibilidade do PostgreSQL
RUN apt-get update && apt-get install -y postgresql-client && apt-get clean

COPY . .

# Comando de entrada
CMD ["sh", "./docker/entrypoint.sh"]