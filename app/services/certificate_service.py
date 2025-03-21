from app.models import Certificate
from app.utils.cpf_validator import normalizar_cpf
import urllib.parse

class CertificateService:
    """Serviço para operações relacionadas a certificados"""
    
    @staticmethod
    def buscar_certificados(cpf_input, estado=None):
        """
        Busca certificados pelo CPF, opcionalmente filtrando por estado
        
        Args:
            cpf_input (str): CPF do usuário (pode estar formatado ou não)
            estado (str, optional): Estado para filtrar os resultados
            
        Returns:
            dict: Dicionário com certificados e total, ou erro
        """
        # Normalizar CPF
        cpf = normalizar_cpf(cpf_input)
        if not cpf:
            return {"erro": "CPF inválido"}, 400
            
        try:
            # Buscar certificados
            resultados = Certificate.find_by_cpf(cpf, estado)
            
            if resultados:
                # Processar resultados
                for certificado in resultados:
                    # Adicionar ID específico para cada certificado
                    curso_url = urllib.parse.quote(certificado['curso'])
                    cpf_url = urllib.parse.quote(certificado['cpf'])
                    certificado['certificado_id'] = f"{cpf_url}/{curso_url}"
                
                return {
                    "certificados": resultados,
                    "total": len(resultados)
                }, 200
            else:
                return {"erro": "Certificado não encontrado"}, 404
                
        except Exception as e:
            return {"erro": f"Erro ao buscar certificado: {str(e)}"}, 500