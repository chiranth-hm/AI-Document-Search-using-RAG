"""FAISS vector store (local)."""
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from app.config import settings
from app.embeddings import get_embedding_model


def get_or_create_faiss_store():
    path = settings.FAISS_INDEX_PATH
    if path.exists():
        return FAISS.load_local(
            str(settings.FAISS_INDEX_DIR),
            get_embedding_model(),
            allow_dangerous_deserialization=True,
        )
    return None


def create_faiss_from_documents(docs: list[Document]) -> FAISS:
    vs = FAISS.from_documents(docs, get_embedding_model())
    vs.save_local(str(settings.FAISS_INDEX_DIR))
    return vs


def add_documents_to_faiss(docs: list[Document]) -> FAISS:
    existing = get_or_create_faiss_store()
    if existing is None:
        return create_faiss_from_documents(docs)
    existing.add_documents(docs)
    existing.save_local(str(settings.FAISS_INDEX_DIR))
    return existing
