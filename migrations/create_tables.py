import psycopg2
import os
from config.settings import DB_CONFIG

def create_tables():
    """Cria a estrutura inicial de tabelas no banco de dados"""
    print("Conectando ao banco de dados...")
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        print("Conexão estabelecida com sucesso!")

        # Recriar a tabela certificados
        print("Recriando tabela de certificados...")

        # Drop tabela se existir
        cur.execute("DROP TABLE IF EXISTS certificados")
        conn.commit()

        # Criar nova tabela com a estrutura correta
        cur.execute('''
        CREATE TABLE certificados (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            curso VARCHAR(255) NOT NULL,
            cpf VARCHAR(14) NOT NULL,
            link_certificado VARCHAR(512) NOT NULL,
            estado VARCHAR(50) DEFAULT '',
            data_adesao VARCHAR(50) DEFAULT '',
            escola VARCHAR(255) DEFAULT '',
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(cpf, curso)
        );

        CREATE INDEX idx_cpf ON certificados(cpf);
        CREATE INDEX idx_estado ON certificados(estado);
        ''')
        conn.commit()

        print("Tabela recriada com sucesso!")
        
        # Fechar cursor
        cur.close()
        
        return True
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        # Fechar conexão
        if conn:
            conn.close()
            print("Conexão fechada.")