"""Config: only Hugging Face API key + simple defaults."""
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Required: get a free token at https://huggingface.co/settings/tokens
    HUGGINGFACEHUB_API_TOKEN: str = ""

    # Optional overrides
    # Local embeddings (sentence-transformers), no API key
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    # Use a model supported on HF free inference (see https://huggingface.co/inference/models)
    CHAT_MODEL: str = "Qwen/Qwen2.5-7B-Instruct"

    FAISS_INDEX_DIR: Path = Path("./faiss_index")
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K_RETRIEVAL: int = 4

    class Config:
        env_file = ".env"
        extra = "ignore"

    @property
    def FAISS_INDEX_PATH(self) -> Path:
        return self.FAISS_INDEX_DIR / "index.faiss"


settings = Settings()
settings.FAISS_INDEX_DIR.mkdir(parents=True, exist_ok=True)
