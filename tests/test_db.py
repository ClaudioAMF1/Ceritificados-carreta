import psycopg2
import time
import sys
from config.settings import DB_CONFIG

def test_db_connection():
    """Testa a conexão com o banco de dados"""
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            print(f"Tentativa {attempt+1}/{max_attempts}...")
            conn = psycopg2.connect(**DB_CONFIG)
            print("Conexão bem-sucedida!")
            conn.close()
            return True
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(2)

    print("Não foi possível conectar ao banco de dados após várias tentativas.")
    return False

if __name__ == "__main__":
    if test_db_connection():
        sys.exit(0)
    else:
        sys.exit(1)