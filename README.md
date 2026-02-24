# IT Support Orchestrator

API de orquestração conversacional para suporte de TI, desenvolvida com
**FastAPI**.

O sistema recebe mensagens via API REST, classifica a intenção do
usuário, extrai entidades relevantes e executa ações como abertura e
consulta de chamados.\
Foi estruturado com foco em arquitetura limpa, baixo acoplamento e
preparação para integração com sistemas corporativos reais (Service
Desk, AD, IAM, etc.).

------------------------------------------------------------------------

## 🎯 Objetivo do Projeto

Simular um cenário corporativo de atendimento automatizado, onde:

-   Usuários enviam solicitações via chat
-   O sistema identifica a intenção (ex: reset de senha, acesso negado,
    VPN, e-mail)
-   Entidades são extraídas (ex: ticket_id, email, sistema afetado)
-   Ações são executadas via conectores desacoplados
-   Logs estruturados garantem rastreabilidade
-   Dados são persistidos em banco relacional

O foco não é apenas "um chatbot", mas um **motor de orquestração
conversacional corporativo**.

------------------------------------------------------------------------

## 🏗 Arquitetura

Estrutura organizada em camadas para garantir separação de
responsabilidades:

app/ api/ -\> Camada HTTP (rotas) services/ -\> Regras de negócio e
orquestração connectors/ -\> Integrações externas (mockáveis) db/ -\>
Persistência e modelos schemas/ -\> Modelos Pydantic (request/response)
core/ -\> Logging e configurações

### Camadas

-   **API:** recebe requisições e valida payloads
-   **Services:** contém lógica de orquestração
-   **Connectors:** abstração para integração com sistemas externos
-   **DB:** persistência relacional usando SQLModel
-   **Core:** logging estruturado com trace_id

Essa organização permite: - Substituir integrações externas sem alterar
a regra de negócio - Migrar banco de dados com mínima alteração -
Facilitar testes unitários

------------------------------------------------------------------------

## 🧠 Classificação de Intenção (NLU)

Abordagem híbrida:

-   Heurística baseada em palavras-chave
-   Extração de entidades via regex
-   Preparado para futura integração com IA/LLM

Intents implementadas:

-   RESET_PASSWORD
-   ACCESS_DENIED
-   VPN_ISSUE
-   EMAIL_ISSUE
-   TICKET_STATUS
-   SPEAK_HUMAN
-   SMALLTALK
-   UNKNOWN

------------------------------------------------------------------------

## 🔗 Conectores

Simulação de integração com:

-   Service Desk (abertura/consulta de chamado)
-   Directory/Identity (reset de senha)

Permite futura troca por: - ServiceNow - Jira Service Management - Azure
AD - Outros sistemas corporativos

------------------------------------------------------------------------

## 🗄 Persistência

Banco utilizado no MVP: - SQLite

Modelos: - Conversation - Message - Ticket

A camada de acesso utiliza SQLModel, permitindo migração simples para
PostgreSQL em produção.

------------------------------------------------------------------------

## 📊 Observabilidade

O sistema gera:

-   Logs estruturados em JSON
-   trace_id por requisição
-   Correlação entre requisição e ação executada

------------------------------------------------------------------------

## 🚀 Como Executar Localmente

### 1. Criar ambiente virtual

python -m venv venv

Windows: .env`\Scripts`{=tex}ctivate

### 2. Instalar dependências

pip install -r requirements.txt

### 3. Rodar servidor

uvicorn app.main:app --reload

Swagger: http://127.0.0.1:8000/docs

Healthcheck: http://127.0.0.1:8000/health

------------------------------------------------------------------------

## 📥 Exemplo de Requisição

POST `/chat/message`

{ "session_id": "sess-001", "user_id": "user-123", "text": "Estou com
acesso negado no WinSCP. Permission denied.", "channel": "web",
"metadata": {} }

------------------------------------------------------------------------

## 📈 Escalabilidade

A aplicação é stateless e pode escalar horizontalmente.

Evoluções previstas:

-   PostgreSQL
-   Cache (Redis)
-   Fila assíncrona (RabbitMQ/Kafka)
-   Centralização de logs (ELK/Datadog)
-   Autenticação JWT

------------------------------------------------------------------------

## 🛣 Roadmap

-   Persistência completa de tickets
-   Endpoint de histórico por sessão
-   Testes automatizados (pytest)
-   Dockerfile e docker-compose
-   Integração com LLM
-   Rate limiting
-   Autenticação

------------------------------------------------------------------------

## 🧩 Tecnologias Utilizadas

-   Python
-   FastAPI
-   SQLModel
-   Pydantic
-   Uvicorn

------------------------------------------------------------------------

## 👩‍💻 Autora
GitHub: https://github.com/02kaede
