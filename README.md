# Sistema de Certificados - Carreta Digital

Este sistema permite gerenciar e consultar certificados emitidos pelo programa Carreta Digital através de uma interface web simples. Os usuários podem buscar seus certificados utilizando o CPF e fazer o download dos mesmos.

## Requisitos

- Docker (versão 19.03 ou superior)
- Docker Compose (versão 1.27 ou superior)

## Estrutura do Projeto

O sistema é composto por:
- Aplicação web em Flask
- Banco de dados PostgreSQL
- Scripts de importação e gerenciamento de dados

### Estrutura de Diretórios Completa

```
├── app/                      # Pasta principal da aplicação
│   ├── __init__.py           # Inicialização da aplicação Flask
│   ├── routes.py             # Rotas da API e páginas
│   ├── models.py             # Modelos e funções relacionadas ao banco de dados
│   ├── utils/                # Utilitários diversos
│   │   ├── __init__.py
│   │   ├── cpf_validator.py  # Funções para validação de CPF
│   │   └── file_processor.py # Funções para processamento de arquivos
│   └── services/             # Serviços da aplicação
│       ├── __init__.py
│       └── certificate_service.py # Lógica de negócio relacionada a certificados
├── config/                   # Configurações da aplicação
│   ├── __init__.py
│   └── settings.py           # Configurações gerais
├── migrations/               # Scripts para migração do banco de dados
│   ├── __init__.py
│   ├── create_tables.py      # Script para criar tabelas do banco
│   └── import_data.py        # Script para importar dados CSV
├── static/                   # Arquivos estáticos
│   ├── css/
│   │   └── style.css         # Estilos da aplicação
│   ├── js/
│   │   └── main.js           # JavaScript para interação do frontend
│   └── image/                # Imagens do sistema
│       ├── logo_Carreta_Digital.png
│       └── logo_carreta.ico
├── templates/                # Templates HTML
│   └── index.html            # Página principal da aplicação
├── tests/                    # Testes automatizados
│   ├── __init__.py
│   ├── test_api.py           # Testes da API
│   └── test_db.py            # Testes de conexão com banco de dados
├── data/                     # Diretório para dados
│   ├── .gitkeep              # Marcador para garantir que o diretório seja incluído no git
│   └── base_dados.csv        # Arquivo CSV com dados dos certificados
├── docker/                   # Arquivos relacionados ao Docker
│   ├── Dockerfile            # Configuração da imagem Docker
│   └── entrypoint.sh         # Script de inicialização
├── .dockerignore             # Arquivos a serem ignorados pelo Docker
├── .gitignore                # Arquivos a serem ignorados pelo Git
├── docker-compose.yml        # Configuração do Docker Compose
├── requirements.txt          # Dependências do projeto
├── app.py                    # Ponto de entrada da aplicação
├── migrate.py                # Script para executar migrações manualmente
├── reorganize.sh             # Script para reorganizar o projeto (opcional)
└── README.md                 # Documentação principal do projeto
```

### Arquivos Principais e suas Funções:

| Arquivo | Função |
|---------|--------|
| `app.py` | Ponto de entrada principal da aplicação, inicializa o servidor Flask |
| `app/routes.py` | Define todas as rotas HTTP e APIs da aplicação |
| `app/models.py` | Implementa a interface com o banco de dados e modelos de dados |
| `config/settings.py` | Centraliza todas as configurações da aplicação |
| `migrations/create_tables.py` | Script para criar/recriar a estrutura do banco de dados |
| `migrations/import_data.py` | Script para importar dados do CSV para o banco |
| `templates/index.html` | Interface web principal para busca de certificados |
| `static/js/main.js` | Lógica de frontend para interação com o usuário |
| `docker-compose.yml` | Configura os serviços Docker (web e banco de dados) |
| `docker/Dockerfile` | Define a imagem Docker para a aplicação |
| `docker/entrypoint.sh` | Script executado na inicialização do contêiner

## Passo a Passo Completo para Instalação e Execução

### 1. Preparação Inicial

1. Clone ou copie todos os arquivos do repositório para sua máquina
   ```
   git clone [URL_DO_REPOSITORIO] Certificados-carreta
   ```
   ou descompacte o arquivo ZIP recebido

2. Navegue até o diretório do projeto
   ```
   cd Certificados-carreta
   ```

3. Crie uma pasta para os dados (se não existir)
   ```
   mkdir -p data
   ```

4. Coloque o arquivo CSV com os dados dos certificados na pasta `data` com o nome `base_dados.csv`

### 2. Configuração das Permissões

1. Torne o script de entrada executável
   ```
   chmod +x docker/entrypoint.sh
   ```

2. Se estiver usando o script de reorganização, torne-o executável
   ```
   chmod +x reorganize.sh
   ```

3. Verifique se o usuário atual tem permissões para os diretórios
   ```
   sudo chown -R $(whoami):$(whoami) .
   ```

4. Defina permissões corretas para diretórios de dados
   ```
   chmod -R 755 data
   ```

### 3. Construção e Inicialização dos Contêineres

1. Construa as imagens Docker (necessário apenas na primeira vez ou após alterações no Dockerfile)
   ```
   docker-compose build
   ```

2. Inicie os contêineres Docker
   ```
   docker-compose up -d
   ```

3. Verifique se os contêineres estão rodando corretamente
   ```
   docker-compose ps
   ```
   Você deve ver dois contêineres ativos: `db` e `web`

### 4. Verificação do Banco de Dados

1. Aguarde cerca de 30 segundos para o PostgreSQL inicializar completamente

2. Verifique os logs para garantir que a inicialização ocorreu corretamente
   ```
   docker-compose logs web
   ```

3. Verifique se o banco de dados foi configurado corretamente (você deve ver mensagens de sucesso nos logs)
   ```
   docker-compose logs | grep "Banco de dados configurado com sucesso"
   ```

### 5. Acesso à Aplicação

1. Acesse a aplicação através do navegador:
   ```
   http://localhost:5000
   ```

2. A página inicial mostrará a interface de busca de certificados

### 6. Solução de Problemas (se necessário)

Se encontrar problemas com a exibição de certificados:

1. Verifique os logs para identificar erros
   ```
   docker-compose logs web
   ```

2. Reinicie a aplicação web
   ```
   docker-compose restart web
   ```

3. Se necessário, force a recriação da tabela e importação dos dados
   ```
   docker-compose exec web python migrate.py
   ```

## Comandos Úteis

- Para verificar os logs contínuos da aplicação:
  ```
  docker-compose logs -f web
  ```

- Para verificar os logs do banco de dados:
  ```
  docker-compose logs db
  ```

- Para parar a aplicação mantendo os dados:
  ```
  docker-compose stop
  ```

- Para parar a aplicação e remover os contêineres (mantém os volumes/dados):
  ```
  docker-compose down
  ```

- Para parar a aplicação e remover TUDO (inclusive dados):
  ```
  docker-compose down -v
  ```

- Para reiniciar a aplicação:
  ```
  docker-compose restart
  ```

- Para entrar no contêiner da aplicação:
  ```
  docker-compose exec web bash
  ```

- Para entrar no banco de dados diretamente:
  ```
  docker-compose exec db psql -U certificados_user -d certificados_db
  ```

## Solução de Problemas Comuns

### Erro de permissão no entrypoint.sh
- Solução: Execute `chmod +x docker/entrypoint.sh` no sistema hospedeiro

### Banco de dados não está acessível
- Solução: Espere mais tempo para a inicialização ou reinicie os contêineres com `docker-compose restart`
- Verifique com `docker-compose logs db` se o PostgreSQL está funcionando corretamente

### Não consegue visualizar todos os certificados
- Solução: Verifique os logs com `docker-compose logs web` para identificar possíveis erros
- Force a recriação do banco com `docker-compose exec web python migrate.py`

### Erro ao importar os dados
- Verifique se o arquivo CSV está no formato correto
- Verifique se o arquivo CSV está no diretório `data/` com o nome `base_dados.csv`
- Verifique permissões: `sudo chmod 644 data/base_dados.csv`

### A aplicação não abre no navegador
- Verifique se a porta 5000 está disponível no sistema hospedeiro com `netstat -tuln | grep 5000`
- Verifique se os contêineres estão rodando com `docker-compose ps`
- Verifique os logs com `docker-compose logs web`

### Problemas com Docker no Windows
- Se estiver usando WSL2, certifique-se de que o Docker Desktop está configurado para integração com WSL2
- Caminhos podem precisar ser ajustados para formato Windows se não estiver usando WSL

## Estrutura dos Dados

O sistema espera um arquivo CSV com os seguintes campos:
- Nome: Nome completo do aluno
- CPF: CPF do aluno
- Curso: Nome do curso realizado
- LINK DRIVE ou Certificado: Link para o certificado
- ESTADO: Estado onde o curso foi realizado (opcional)
- Data de Adesão: Data de adesão ao programa (opcional)
- Escola: Instituição de ensino (opcional)

## Observações Importantes

- Cada aluno (CPF) pode ter múltiplos certificados
- O sistema normaliza o CPF automaticamente para o formato XXX.XXX.XXX-XX
- Os links do Google Drive são convertidos para links diretos de download
- Todo o sistema está configurado para funcionar dentro de contêineres Docker, minimizando dependências no host

## Arquitetura do Sistema

### Componentes Principais

1. **Frontend**
   - Interface web responsiva construída com HTML, CSS e JavaScript
   - Formulário de busca por CPF com validação em tempo real
   - Exibição de múltiplos certificados por usuário
   - Links diretos para download dos certificados

2. **Backend (Flask)**
   - API RESTful para consulta de certificados
   - Processamento de CPF e normalização
   - Roteamento para download de certificados
   - Estatísticas de uso do sistema

3. **Banco de Dados (PostgreSQL)**
   - Armazenamento persistente dos dados de certificados
   - Índices otimizados para busca por CPF
   - Relacionamento de um-para-muitos entre CPF e certificados

4. **Serviços Auxiliares**
   - Script de importação para processamento de CSV
   - Utilitários para validação e formatação de dados
   - Conversão de links do Google Drive para formato acessível

### Fluxo de Dados

1. O usuário insere seu CPF na interface web
2. A aplicação normaliza o CPF e consulta o banco de dados
3. Os certificados encontrados são exibidos em formato de cards
4. O usuário pode baixar qualquer certificado através do link fornecido
5. Os links do Google Drive são automaticamente convertidos para formato adequado

### Diagrama Simplificado

```
+-------------------+        +------------------+        +------------------+
|                   |        |                  |        |                  |
|  Interface Web    |<------>|  API Flask       |<------>|  PostgreSQL      |
|  (HTML/JS/CSS)    |        |  (Python)        |        |  (Banco de Dados)|
|                   |        |                  |        |                  |
+-------------------+        +------------------+        +------------------+
                                     ^
                                     |
                             +------------------+
                             |                  |
                             |  Importação CSV  |
                             |  (Scripts Python)|
                             |                  |
                             +------------------+
```

## Backup e Restauração

### Para fazer backup do banco de dados:
```
docker-compose exec db pg_dump -U certificados_user certificados_db > backup_$(date +%Y%m%d).sql
```

### Para restaurar um backup:
```
cat backup_file.sql | docker-compose exec -T db psql -U certificados_user -d certificados_db
```

### Backup completo com dados e imagens Docker:

1. Backup do volume de dados do PostgreSQL
   ```
   docker run --rm -v sistema-certificados_postgres_data:/volume -v $(pwd)/backups:/backup alpine tar -czvf /backup/postgres_data_$(date +%Y%m%d).tar.gz -C /volume ./
   ```

2. Backup da pasta de dados CSV
   ```
   tar -czvf backups/data_csv_$(date +%Y%m%d).tar.gz data/
   ```

3. Salvar as imagens Docker como arquivos
   ```
   docker save -o backups/images_$(date +%Y%m%d).tar sistema-certificados_web postgres:14
   ```

### Restauração completa:

1. Restaurar imagens Docker
   ```
   docker load -i backups/images_[DATA].tar
   ```

2. Restaurar dados CSV
   ```
   tar -xzvf backups/data_csv_[DATA].tar.gz -C .
   ```

3. Parar serviços ativos e remover volume existente
   ```
   docker-compose down -v
   ```

4. Recriar volume vazio
   ```
   docker volume create sistema-certificados_postgres_data
   ```

5. Restaurar dados do PostgreSQL
   ```
   docker run --rm -v sistema-certificados_postgres_data:/volume -v $(pwd)/backups:/backup alpine tar -xzvf /backup/postgres_data_[DATA].tar.gz -C /volume
   ```

6. Reiniciar serviços
   ```
   docker-compose up -d
   ```

## Desenvolvimento

### Configuração do Ambiente de Desenvolvimento

Para desenvolver ou modificar o sistema:

1. Clone o repositório
   ```
   git clone [URL_DO_REPOSITORIO] sistema-certificados
   cd sistema-certificados
   ```

2. Instale as dependências em um ambiente virtual
   ```
   # Criar ambiente virtual
   python -m venv venv
   
   # Ativar ambiente virtual
   # No Linux/Mac:
   source venv/bin/activate
   # No Windows:
   venv\Scripts\activate
   
   # Instalar dependências
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente para desenvolvimento local
   ```
   # No Linux/Mac:
   export DB_USER=certificados_user
   export DB_PASSWORD=certificados_pwd
   export DB_HOST=localhost
   export DB_PORT=5432
   export DB_NAME=certificados_db
   export DEBUG=True
   
   # No Windows (PowerShell):
   $env:DB_USER="certificados_user"
   $env:DB_PASSWORD="certificados_pwd"
   $env:DB_HOST="localhost"
   $env:DB_PORT="5432"
   $env:DB_NAME="certificados_db"
   $env:DEBUG="True"
   ```

4. Configure o PostgreSQL local (ou use o Docker apenas para o banco)
   ```
   # Iniciar apenas o serviço de banco de dados
   docker-compose up -d db
   ```

5. Execute os scripts de migração de banco de dados
   ```
   python -m migrations.create_tables
   python -m migrations.import_data
   ```

6. Inicie a aplicação em modo de desenvolvimento
   ```
   python app.py
   ```

### Fluxo de Desenvolvimento

1. Faça alterações no código
2. Execute testes para verificar se a funcionalidade está correta
   ```
   # Executar testes de API
   python -m tests.test_api
   
   # Executar testes de conexão com banco
   python -m tests.test_db
   ```
3. Reconstrua os contêineres Docker se necessário
   ```
   docker-compose build
   docker-compose up -d
   ```

### Formatação e Boas Práticas

- Siga a PEP 8 para codificação em Python
- Use comentários para documentar funções e trechos complexos
- Mantenha a estrutura modular, separando responsabilidades
- Documente novos endpoints de API no README

### Notas para Contribuidores

- Mantenha a compatibilidade com Docker para facilitar a implantação
- Ao adicionar novas dependências, atualize o requirements.txt
  ```
  pip freeze > requirements.txt
  ```
- Qualquer modificação no modelo de dados deve incluir atualizações nos scripts de migração

## Requisitos Técnicos Detalhados

### Dependências Python

- Flask 2.0.1: Framework web para API e interface de usuário
- Werkzeug 2.0.3: Biblioteca WSGI para o Flask
- Jinja2 3.0.3: Motor de templates para o Flask
- psycopg2-binary 2.9.3: Adaptador PostgreSQL para Python
- gunicorn 20.1.0: Servidor WSGI para produção
- python-dotenv 0.19.2: Carregamento de variáveis de ambiente

### Requisitos de Banco de Dados

- PostgreSQL 14 ou superior
- Extensões requeridas:
  - pg_isready: Para verificar disponibilidade do banco
  - psql: Para operações de linha de comando

### Requisitos de Hardware (Mínimo Recomendado)

- CPU: 2 cores
- RAM: 2GB
- Armazenamento: 1GB livre para a aplicação + espaço para os dados

### Portas e Comunicação

- 5000: Frontend e API (web)
- 5432: PostgreSQL (interno)

### Requisitos para Implantação em Produção

1. **Segurança**
   - Usar HTTPS em ambiente de produção
   - Configurar um servidor reverso proxy (Nginx ou Apache)
   - Ajustar as variáveis de ambiente (DEBUG=False)

2. **Escalabilidade**
   - Configurar gunicorn com múltiplos workers
   - Adicionar balanceamento de carga para múltiplas instâncias

3. **Monitoramento**
   - Implementar logging para registrar acessos e erros
   - Configurar sistema de monitoramento para disponibilidade

## Licença

Este projeto é distribuído sob licença proprietária. Todos os direitos reservados.

© 2025 RBCIP | Carreta Digital | Ministério das Comunicações | Governo Federal
