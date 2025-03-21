# Este arquivo permite que o diretório migrations seja um pacote Python
from migrations.create_tables import create_tables
from migrations.import_data import import_data

def setup_database():
    """Configura o banco de dados com tabelas e dados iniciais"""
    # Criar tabelas
    if create_tables():
        # Importar dados
        import_data()
        return True
    return False