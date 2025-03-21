import unittest
import json
from app import create_app
from app.utils.cpf_validator import normalizar_cpf

class ApiTestCase(unittest.TestCase):
    """Testes para a API do sistema de certificados"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
    
    def test_index_page(self):
        """Testa se a página inicial carrega corretamente"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_estados_endpoint(self):
        """Testa o endpoint de listagem de estados"""
        response = self.client.get('/estados')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('estados', data)
    
    def test_buscar_certificado_sem_cpf(self):
        """Testa busca de certificado sem fornecer CPF"""
        response = self.client.post('/certificado', 
                                    data=json.dumps({}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('erro', data)
    
    def test_cpf_normalization(self):
        """Testa a normalização de CPF"""
        # CPF sem formatação
        self.assertEqual(normalizar_cpf('12345678901'), '123.456.789-01')
        # CPF com formatação
        self.assertEqual(normalizar_cpf('123.456.789-01'), '123.456.789-01')
        # CPF inválido (muito curto)
        self.assertIsNone(normalizar_cpf('123'))
        # CPF vazio
        self.assertIsNone(normalizar_cpf(''))
        # CPF None
        self.assertIsNone(normalizar_cpf(None))

if __name__ == '__main__':
    unittest.main()