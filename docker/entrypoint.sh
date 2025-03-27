#!/bin/bash
set -e

echo "Aguardando o PostgreSQL..."
# Usar variáveis de ambiente para conexão
for i in {1..30}; do
    if pg_isready -h db -U ${DATABASE_USER} -d ${DATABASE_NAME}; then
        echo "PostgreSQL está pronto!"
        break
    fi
    echo "Aguardando o PostgreSQL... ($i/30)"
    sleep 2
done

echo "Verificando conexão com o banco de dados..."
python -m tests.test_db

echo "Configurando o banco de dados..."
# Executa as migrações
python migrate.py

echo "Iniciando a aplicação..."
# Execute o aplicativo web
python app.py