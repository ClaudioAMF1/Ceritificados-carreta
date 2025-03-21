import csv
import os
import psycopg2
from config.settings import DB_CONFIG, CSV_FILE
from app.utils.cpf_validator import normalizar_cpf
from app.utils.file_processor import formatar_link_direto

def import_data(arquivo_csv=CSV_FILE):
    """
    Importa dados do CSV para o banco de dados
    
    Args:
        arquivo_csv (str): Caminho para o arquivo CSV
        
    Returns:
        bool: True se a importação foi bem-sucedida, False caso contrário
    """
    # Verificar se o arquivo existe
    if not os.path.exists(arquivo_csv):
        print(f"Arquivo não encontrado: {arquivo_csv}")
        return False
    
    # Conectar ao banco de dados
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        print(f"Processando CSV: {arquivo_csv}...")
        
        # Tentar diferentes encodings
        encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
        file_content = None
        
        for encoding in encodings:
            try:
                with open(arquivo_csv, 'r', encoding=encoding) as f:
                    # Ler apenas algumas linhas para testar o encoding
                    sample = f.read(1024)
                    if sample:  # Se conseguiu ler, resetar o arquivo
                        file_encoding = encoding
                        break
            except UnicodeDecodeError:
                continue
        
        if not file_encoding:
            print("Não foi possível determinar o encoding do arquivo CSV.")
            return False
            
        # Processar CSV com o encoding correto
        with open(arquivo_csv, 'r', encoding=file_encoding) as f:
            reader = csv.DictReader(f)
            
            # Processo de importação
            registros_validos = 0
            registros_invalidos = 0
            
            for i, row in enumerate(reader):
                try:
                    nome = row.get('Nome', '').strip()
                    cpf_raw = row.get('CPF', '')
                    cpf = normalizar_cpf(cpf_raw)
                    curso = row.get('Curso', '').strip()
                    
                    # Verificar qual coluna tem o link do certificado
                    link_raw = None
                    if 'LINK DRIVE' in row and row['LINK DRIVE']:
                        link_raw = row['LINK DRIVE'].strip()
                    elif 'Certificado' in row and row['Certificado']:
                        link_raw = row['Certificado'].strip()
                    
                    link = formatar_link_direto(link_raw) if link_raw else None
                    estado = row.get('ESTADO', '').strip()
                    data_adesao = row.get('Data de Adesão', '').strip()
                    escola = row.get('Escola', '').strip()
                    
                    # Verificar dados obrigatórios
                    if nome and cpf and curso and link:
                        try:
                            # Usar ON CONFLICT com chave composta (cpf, curso)
                            cur.execute('''
                            INSERT INTO certificados 
                            (nome, curso, cpf, link_certificado, estado, data_adesao, escola)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (cpf, curso) DO UPDATE 
                            SET nome = EXCLUDED.nome,
                                link_certificado = EXCLUDED.link_certificado,
                                estado = EXCLUDED.estado,
                                data_adesao = EXCLUDED.data_adesao,
                                escola = EXCLUDED.escola
                            ''', (nome, curso, cpf, link, estado, data_adesao, escola))
                            registros_validos += 1
                            
                            # Commit a cada 100 registros
                            if registros_validos % 100 == 0:
                                conn.commit()
                                print(f'Processados {registros_validos} registros...')
                        except Exception as e:
                            registros_invalidos += 1
                            print(f'Erro ao inserir {nome} (CPF: {cpf}, Curso: {curso}): {e}')
                    else:
                        registros_invalidos += 1
                        razoes = []
                        if not nome:
                            razoes.append("sem nome")
                        if not cpf:
                            razoes.append(f"CPF inválido ({cpf_raw})")
                        if not curso:
                            razoes.append("sem curso")
                        if not link:
                            razoes.append("sem link de certificado")
                        
                        print(f'Registro inválido linha {i+2}: {", ".join(razoes)}')
                except Exception as e:
                    registros_invalidos += 1
                    print(f'Erro ao processar linha {i+2}: {e}')
            
            # Commit final
            conn.commit()
            
            # Verificar total de registros
            cur.execute('SELECT COUNT(*) FROM certificados')
            total = cur.fetchone()[0]
            
            print(f'\nImportação concluída!')
            print(f'Registros válidos importados: {registros_validos}')
            print(f'Registros inválidos: {registros_invalidos}')
            print(f'Total na tabela certificados: {total}')
            
            # Verificar quantos alunos distintos
            cur.execute('SELECT COUNT(DISTINCT cpf) FROM certificados')
            total_alunos = cur.fetchone()[0]
            print(f'Total de alunos distintos: {total_alunos}')
            
            # Verificar alunos com múltiplos certificados
            cur.execute('''
            SELECT cpf, nome, COUNT(*) as total 
            FROM certificados 
            GROUP BY cpf, nome 
            HAVING COUNT(*) > 1 
            ORDER BY total DESC 
            LIMIT 5
            ''')
            alunos_multi = cur.fetchall()
            if alunos_multi:
                print("\nExemplos de alunos com múltiplos certificados:")
                for aluno in alunos_multi:
                    print(f"- {aluno[1]} (CPF: {aluno[0]}, Certificados: {aluno[2]})")
                    # Mostrar os cursos do aluno
                    cur.execute('SELECT curso FROM certificados WHERE cpf = %s', (aluno[0],))
                    cursos = [c[0] for c in cur.fetchall()]
                    print(f"  Cursos: {', '.join(cursos[:3])}...")
            
        # Fechar cursor
        cur.close()
        return True
        
    except Exception as e:
        print(f"Erro durante importação: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        # Fechar conexão
        if conn:
            conn.close()