# RAG Demonstrator

Um demonstrador web da técnica de Retrieval Augmented Generation (RAG), desenvolvido como parte do Trabalho de Conclusão de Curso (TCC) do Curso de Ciência da Computação da Universidade Paulista (UNIP)

# Overview

RAG consiste na combinação entre recuperação de dados e modelos de linguagem de grande escala.

Ao invés de depender exclusivamente em dados armazenados nos parâmetros do modelo, o sistema busca passagens relevantes em uma base de conhecimentos externa e os providencia como contexto para o modelo de linguagem antes de gerar uma resposta.

Esse projeto foi desenvolvido como um demonstrador educacional, com a intenção de tornar esses processos observáveis em uma interface visual.

# Funções

- UI para comunicação com a IA
- Pipeline RAG
- Busca semântica usando embeddings de documentos relevantes
- Base de dados de vetores para armazenamento e recuperação de documentos.
- API da OpenAI para integração.
- Ingestion de PDFs
- Visualização de chunks de documentos recuperados.
- Display da fonte dos documentos, página, chunk e distância do vetor.
- Visualização do contexto construído e providenciado ao modelo.
- Visualização da resposta gerada.
- Histórico de conversa baseado na sessão atual.
- Inspetor da execução de RAG para perguntas préviamente enviadas.
- Execução local do backend e frontend.

# Arquitetura backend

Implementada em Python utilizando FastAPI.

1. Recebe a pergunta do usuário.
2. Gera um embedding para a questão.
3. Busca chunks de documentos que sejam semânticamente similares no banco de vetores.
4. Constrói um contexto baseado nos documentos recuperados.
5. Envia a pergunta e os documetnos recuperados para o modelo.
6. Retorna a reposta gerada com as informações pertinentes à recuperação de dados feita durante o processo.

# Arquitetura frontend

Implementado utilizando React.

- Interface de chat.
- Histórico de conversa.
- Visualização de documentos recuperados.
- Visualização do pipeline RAG.
- Visualização do contexto contruído.
- Visualização da resposta gerada.

# Pipeline RAG

Pergunta do Usuário
\/
Embedding da pergunta
\/
Base de Vetores
\/
Chunks relevantes
\/
Construção de contexto
\/
Modelo OpenAI
\/
Resposta gerada

# Estrutura

PROJETO/
│
├── backend/
│   ├── app/
│   │   ├── embeddings.py
│   │   ├── llm.py
│   │   ├── main.py
│   │   ├── rag.py
│   │   ├── search.py
│   │   └── vector_store.py
│   │
│   ├── scripts/
│   │   └── ingest.py
│   │
│   ├── data/
│   │   └── papers/
│   │
│   ├── .env
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── App.css
│   │
│   ├── package.json
│   └── ...
│
├── .gitignore
└── README.md

# Requisitos

- Python 3.11 ou mais recente
- Node.js e npm
- Git
- Cadastro na OpenAI API com acesso a API

O projeto foi desenvolvido e testado localmente em Windows.

# Chave OpenAI API

O projeto utiliza a API para geração de embeddings e reposta de modelos.

**** Uma chave para a OpenAI API é necessária para rodar o backend ****

Por motivos de segurança, a chave utilizada no desenvolvimento NÃO está inclusa nesse repositório.

- Crie um arquivo .env dentro do diretório /backend com a variável: OPENAI_API_KEY=sua_chave_de_api_aqui

- Não commite esse arquivo.

- Usuários rodando sua própria cópia do projeto devem providenciar sua própria chave da API.

# Setup do backend

1. Abra o terminal e navegue ao diretório /backend:
pwsh-> cd backend
2. Crie um venv Python:
pwsh-> python -m venv .venv
3. Ative o venv:
pwsh-> .\.venv\Scripts\Activate.ps1
4. Instale as dependências:
pwsh-> pip install -r requirements.txt
5. Configure a chave da API em:
backend/.env

- Ingestion de documentos

1. Coloque os PDFs desejados (já providenciados documentos relevantes sobre RAG) em:
backend/data/papers/
2. Rode o script de ingestion:
pwsh-> python -m scripts.ingest

- Inicie a API

No diretório backend, rode:
pwsh-> uvicorn app.main:app --reload --port 8000

A API ficará disponível em:
http://localhost:8000

A documentação FastAPI ficará disponível em:
http://localhost:8000/docs

# Setup do frontend

1. Abra outro terminal e navegue ao diretório /frontend:
pwsh-> cd frontend

2. Instale o Node.js e dependências:
pwsh-> npm intall

3. Inicie o servidor de desenvolvimento:
pwsh-> npm run dev

O frontend ficará disponível em:
http://localhost:5173

# Autor

Mario Rossi Bracco da Costa - Universidade Paulista (UNIP)

# Licensa

Esse projeto foi desenvolvido com propósitos acadêmicos.



