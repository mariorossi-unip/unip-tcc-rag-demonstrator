from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.rag import ask_rag
from app.search import search_documents

app = FastAPI(
    title="RAG TCC API",
    description="API para o projeto de TCC utilizando RAG (Retrieval-Augmented Generation).",
    version="0.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# RESPONSE MODELS
class AskRequest(BaseModel):
    question: str = Field(
        min_length=1,
        description="Pergunta do usuário para o sistema RAG."
    )

    n_results: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Número de chunks a serem retornados da busca semântica."
    )

class SearchRequest(BaseModel):
    query: str = Field(
        min_length=1,
        description="Consulta do usuário para a busca semântica."
    )

    n_results: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Número de chunks a serem retornados da busca semântica."
    )

#HEALTH

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

#SEARCH ONLY

@app.post("/search")
def search(request: SearchRequest):
    "Executa apenas a busca semântica do pipeline RAG"

    try:
        results = search_documents(
            query=request.query,
            n_results=request.n_results
        )
        return {
            "query": request.query,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#PIPELINE RAG COMPLETA

@app.post("/ask")
def ask(request: AskRequest):
    """
    Executa o pipeline completo RAG: busca semântica + geração de resposta.
    """

    try:
        result = ask_rag(
            question=request.question,
            n_results=request.n_results
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))