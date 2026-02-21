"""RAG: FAISS retriever + Hugging Face chat (API key only)."""
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from huggingface_hub.errors import BadRequestError

from app.config import settings
from app.store import get_or_create_faiss_store


def _format_docs(docs):
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


def get_rag_chain():
    vectorstore = get_or_create_faiss_store()
    if vectorstore is None or not settings.HUGGINGFACEHUB_API_TOKEN:
        return None

    retriever = vectorstore.as_retriever(search_kwargs={"k": settings.TOP_K_RETRIEVAL})
    endpoint = HuggingFaceEndpoint(
        repo_id=settings.CHAT_MODEL,
        task="text-generation",
        max_new_tokens=512,
        temperature=0.2,
    )
    llm = ChatHuggingFace(llm=endpoint)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer using only the context below. If the context doesn't help, say so. Don't make things up."),
        ("human", "Context:\n{context}\n\nQuestion: {question}"),
    ])

    chain = (
        {"context": retriever | _format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain, retriever


def query_rag(question: str) -> tuple[str, list]:
    result = get_rag_chain()
    if result is None:
        if not settings.HUGGINGFACEHUB_API_TOKEN:
            return "Set HUGGINGFACEHUB_API_TOKEN in .env (get a free token at https://huggingface.co/settings/tokens).", []
        return "Upload at least one PDF first, then ask questions.", []
    chain, retriever = result
    source_docs = retriever.invoke(question)
    try:
        answer = chain.invoke(question)
    except BadRequestError as e:
        msg = str(e)
        if "model_not_supported" in msg or "not supported by any provider" in msg:
            return (
                f"Chat model '{settings.CHAT_MODEL}' isn't available on your account. "
                "Try another model: set CHAT_MODEL in .env to e.g. Qwen/Qwen2.5-7B-Instruct or meta-llama/Llama-3.2-3B-Instruct. "
                "See https://huggingface.co/inference/models",
                [{"content": d.page_content, "metadata": d.metadata} for d in source_docs],
            )
        return f"Chat request failed: {msg}", []
    sources = [{"content": d.page_content, "metadata": d.metadata} for d in source_docs]
    return answer, sources
