"""Embeddings: local sentence-transformers (free, no API key). Hugging Face API is used only for chat."""
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from app.config import settings


def get_embedding_model():
    """Local model - no API key, runs on CPU. First run downloads ~80MB."""
    return HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
