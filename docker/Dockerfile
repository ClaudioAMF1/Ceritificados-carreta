FROM python:3.10-slim

WORKDIR /app

# Copiar requirements.txt primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt && \
    apt-get update && \
    apt-get install -y postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copiar o código da aplicação
COPY . .

# Tornar o script de entrada executável
RUN chmod +x docker/entrypoint.sh

# Comando de entrada
CMD ["sh", "./docker/entrypoint.sh"]