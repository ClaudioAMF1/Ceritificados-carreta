import re

def normalizar_cpf(cpf):
    """Remove caracteres não numéricos do CPF e formata corretamente"""
    if not cpf:
        return None
        
    # Remover caracteres não numéricos
    clean_cpf = re.sub(r'\D', '', str(cpf))
    
    # Verificar tamanho e ajustar se necessário
    if len(clean_cpf) < 9:
        return None
        
    if len(clean_cpf) < 11:
        clean_cpf = clean_cpf.zfill(11)
    elif len(clean_cpf) > 11:
        clean_cpf = clean_cpf[:11]
        
    # Formatar CPF (XXX.XXX.XXX-XX)
    return f'{clean_cpf[:3]}.{clean_cpf[3:6]}.{clean_cpf[6:9]}-{clean_cpf[9:]}'