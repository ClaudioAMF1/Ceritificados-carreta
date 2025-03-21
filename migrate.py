from migrations import setup_database

if __name__ == "__main__":
    print("Iniciando configuração do banco de dados...")
    if setup_database():
        print("Banco de dados configurado com sucesso!")
    else:
        print("Falha na configuração do banco de dados.")