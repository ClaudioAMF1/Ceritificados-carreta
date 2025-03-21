from flask import request, jsonify, redirect, render_template, url_for
from app.models import Certificate
from app.utils.cpf_validator import normalizar_cpf
import urllib.parse

def register_routes(app):
    """Registra todas as rotas da aplicação"""
    
    @app.route('/')
    def index():
        """Página inicial com formulário de consulta"""
        return render_template('index.html')

    @app.route('/estados')
    def listar_estados():
        """Lista os estados disponíveis no banco de dados"""
        try:
            # Buscar estados disponíveis
            estados = Certificate.get_distinct_estados()
            return jsonify({"estados": estados})
        except Exception as e:
            return jsonify({"erro": f"Erro ao buscar estados: {str(e)}"}), 500

    @app.route('/certificado', methods=['POST'])
    def buscar_certificado():
        """Busca certificados pelo CPF"""
        # Obter CPF da requisição
        dados = request.json
        if not dados or 'cpf' not in dados:
            return jsonify({"erro": "CPF não fornecido"}), 400
        
        # Normalizar CPF
        cpf = normalizar_cpf(dados['cpf'])
        if not cpf:
            return jsonify({"erro": "CPF inválido"}), 400
        
        # Filtrar por estado se fornecido
        estado = dados.get('estado', None)
        
        try:
            # Buscar certificados
            resultados = Certificate.find_by_cpf(cpf, estado)
            
            if resultados:
                # Verificar se cada certificado tem um link válido
                for certificado in resultados:
                    # Adicionar ID específico para cada certificado (CPF+Curso para URL)
                    curso_url = urllib.parse.quote(certificado['curso'])
                    cpf_url = urllib.parse.quote(certificado['cpf'])
                    certificado['certificado_id'] = f"{cpf_url}/{curso_url}"
                
                return jsonify({
                    "certificados": resultados,
                    "total": len(resultados)
                })
            else:
                return jsonify({"erro": "Certificado não encontrado"}), 404
                
        except Exception as e:
            return jsonify({"erro": f"Erro ao buscar certificado: {str(e)}"}), 500

    @app.route('/download-certificado/<path:cpf>/<path:curso>', methods=['GET'])
    def download_certificado(cpf, curso):
        """Redirecionamento direto para download do certificado"""
        try:
            # Buscar o certificado específico
            resultado = Certificate.find_by_cpf_and_course(cpf, curso)
            
            if resultado and resultado["link_certificado"]:
                # Redirecionar para o URL do PDF
                return redirect(resultado["link_certificado"])
            else:
                return jsonify({"erro": "Link do certificado não encontrado"}), 404
                
        except Exception as e:
            return jsonify({"erro": f"Erro ao buscar certificado: {str(e)}"}), 500

    @app.route('/estatisticas')
    def estatisticas():
        """Retorna estatísticas sobre certificados no banco de dados"""
        try:
            stats = Certificate.get_statistics()
            return jsonify(stats)
        except Exception as e:
            return jsonify({"erro": f"Erro ao obter estatísticas: {str(e)}"}), 500