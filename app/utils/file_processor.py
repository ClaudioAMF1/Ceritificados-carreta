import re

def extract_drive_id(url):
    """Extrai ID do Google Drive de uma URL"""
    if not url:
        return None
        
    # Padrões para URLs do Google Drive
    patterns = [
        r'id=([a-zA-Z0-9_-]+)',                # formato ?id=
        r'/d/([a-zA-Z0-9_-]+)',                # formato /d/
        r'drive\.google\.com/file/d/([^/]+)',  # formato completo
        r'drive\.google\.com/open\?id=([^&]+)' # formato open?id=
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def formatar_link_direto(url):
    """Converte links do Drive para formato direto de download"""
    drive_id = extract_drive_id(url)
    if drive_id:
        return f"https://drive.google.com/uc?export=download&id={drive_id}"
    return url