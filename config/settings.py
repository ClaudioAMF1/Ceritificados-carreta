import os

# Configuração da conexão com o PostgreSQL
DB_CONFIG = {
    "dbname": os.environ.get("DB_NAME", "certificados_db"),
    "user": os.environ.get("DB_USER", "certificados_user"),
    "password": os.environ.get("DB_PASSWORD", "certificados_pwd"),
    "host": os.environ.get("DB_HOST", "db"),
    "port": os.environ.get("DB_PORT", "5432")
}

# Configurações da aplicação
DEBUG = os.environ.get("DEBUG", "True").lower() in ('true', '1', 't')
PORT = int(os.environ.get("PORT", 5000))

# Configurações de arquivos
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
CSV_FILE = os.path.join(DATA_DIR, 'base_dados.csv')