"""FastAPI app: ingest PDFs, chat with RAG. Uses only Hugging Face API key."""
import os
import traceback
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.ingest import ingest_pdf
from app.models import ChatRequest, ChatResponse, IngestResponse, SourceChunk
from app.rag import query_rag

# So HuggingFaceEndpoint and embeddings can use the token
if settings.HUGGINGFACEHUB_API_TOKEN:
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = settings.HUGGINGFACEHUB_API_TOKEN

app = FastAPI(
    title="AI Document Search (RAG Chatbot)",
    description="Chat with PDFs using LLM + semantic search. One API key: Hugging Face.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "service": "AI Document Search (RAG Chatbot)",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/reset")
def reset():
    try:
        from app.store import reset_faiss_store
        reset_faiss_store()
        return {"success": True, "message": "Vector index cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reset failed: {str(e)}")

@app.post("/ingest", response_model=IngestResponse)
async def ingest(file: UploadFile = File(...)):
    """Upload a PDF; extract text, chunk, embed, and store in FAISS."""
    if not settings.HUGGINGFACEHUB_API_TOKEN:
        raise HTTPException(
            status_code=503,
            detail="Set HUGGINGFACEHUB_API_TOKEN in .env. Get a free token at https://huggingface.co/settings/tokens",
        )
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Empty file.")
    try:
        num_docs, num_chunks = ingest_pdf(contents, filename=file.filename or "document.pdf")
        return IngestResponse(
            success=True,
            message=f"Ingested '{file.filename}'. Added {num_chunks} chunks.",
            num_documents=num_docs,
            num_chunks=num_chunks,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


@app.post("/chat", response_model=ChatResponse)
def chat(body: ChatRequest):
    """Ask a question; get RAG answer and optional sources."""
    answer, sources = query_rag(body.message)
    source_chunks = [SourceChunk(content=s["content"], metadata=s.get("metadata")) for s in sources]
    return ChatResponse(message=answer, sources=source_chunks, done=True)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
