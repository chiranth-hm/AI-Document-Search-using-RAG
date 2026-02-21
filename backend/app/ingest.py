"""PDF ingestion: load, chunk, embed, store in FAISS (all free)."""
import io
from typing import List

import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from app.config import settings
from app.store import add_documents_to_faiss


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text from PDF using PyMuPDF (free)."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text_parts = []
    for page in doc:
        text_parts.append(page.get_text())
    doc.close()
    return "\n".join(text_parts)


def chunk_text(text: str, metadata: dict) -> List[Document]:
    """Split text into overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_text(text)
    return [Document(page_content=c, metadata=metadata) for c in chunks]


def ingest_pdf(pdf_bytes: bytes, filename: str = "document.pdf") -> tuple[int, int]:
    """Ingest one PDF: extract text, chunk, embed, add to FAISS. Returns (num_docs, num_chunks)."""
    text = extract_text_from_pdf(pdf_bytes)
    if not text.strip():
        raise ValueError("No text could be extracted from the PDF.")
    metadata = {"source": filename}
    docs = chunk_text(text, metadata)
    add_documents_to_faiss(docs)
    return 1, len(docs)
