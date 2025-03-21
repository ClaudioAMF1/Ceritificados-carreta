import psycopg2
from psycopg2.extras import RealDictCursor
from config.settings import DB_CONFIG

def get_db_connection():
    """Estabelece conexão com o banco de dados"""
    return psycopg2.connect(**DB_CONFIG)

class Certificate:
    """Classe para gerenciar certificados no banco de dados"""
    
    @staticmethod
    def find_by_cpf(cpf, estado=None):
        """Busca certificados pelo CPF"""
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            if estado:
                cursor.execute(
                    """
                    SELECT 
                        nome, curso, cpf, link_certificado, estado, data_adesao, escola 
                    FROM certificados 
                    WHERE cpf LIKE %s AND estado = %s
                    ORDER BY curso
                    """, 
                    (f"%{cpf}%", estado)
                )
            else:
                cursor.execute(
                    """
                    SELECT 
                        nome, curso, cpf, link_certificado, estado, data_adesao, escola 
                    FROM certificados 
                    WHERE cpf LIKE %s
                    ORDER BY curso
                    """, 
                    (f"%{cpf}%",)
                )
                
            resultados = cursor.fetchall()
            return resultados
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def find_by_cpf_and_course(cpf, curso):
        """Busca certificado específico pelo CPF e curso"""
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cursor.execute(
                "SELECT link_certificado FROM certificados WHERE cpf = %s AND curso = %s", 
                (cpf, curso)
            )
            
            resultado = cursor.fetchone()
            return resultado
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_distinct_estados():
        """Retorna lista de estados distintos"""
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cursor.execute("SELECT DISTINCT estado FROM certificados WHERE estado != '' ORDER BY estado")
            resultados = cursor.fetchall()
            estados = [r['estado'] for r in resultados if r['estado']]
            return estados
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_statistics():
        """Retorna estatísticas sobre certificados"""
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            stats = {}
            
            # Total de certificados
            cursor.execute("SELECT COUNT(*) as total FROM certificados")
            stats['total_certificados'] = cursor.fetchone()['total']
            
            # Total de alunos distintos
            cursor.execute("SELECT COUNT(DISTINCT cpf) as total FROM certificados")
            stats['total_alunos'] = cursor.fetchone()['total']
            
            # Média de certificados por aluno
            if stats['total_alunos'] > 0:
                stats['media_certificados_por_aluno'] = stats['total_certificados'] / stats['total_alunos']
            else:
                stats['media_certificados_por_aluno'] = 0
                
            # Alunos com mais certificados
            cursor.execute("""
                SELECT nome, cpf, COUNT(*) as total_cursos 
                FROM certificados 
                GROUP BY nome, cpf 
                ORDER BY total_cursos DESC 
                LIMIT 5
            """)
            stats['alunos_mais_certificados'] = cursor.fetchall()
            
            # Certificados por estado
            cursor.execute("SELECT estado, COUNT(*) as total FROM certificados GROUP BY estado ORDER BY total DESC")
            stats['por_estado'] = cursor.fetchall()
            
            # Certificados por curso
            cursor.execute("SELECT curso, COUNT(*) as total FROM certificados GROUP BY curso ORDER BY total DESC")
            stats['por_curso'] = cursor.fetchall()
            
            return stats
        finally:
            cursor.close()
            conn.close()