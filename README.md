# AI Document Search (RAG Chatbot)

Chat with PDFs using **LLM + semantic search**. One API key (Hugging Face), no local AI install.

## Stack

| Part       | Tech              |
|-----------|-------------------|
| Frontend  | React, Tailwind   |
| Backend   | FastAPI           |
| AI + embeddings | Hugging Face (API) |
| Vector DB | FAISS (local)     |

## Setup

1. **Get a free API key**  
   [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) → Create token (read is enough).

2. **Backend**
   ```bash
   cd backend
   python -m venv .venv
   .venv\Scripts\activate    # Windows
   pip install -r requirements.txt
   copy .env.example .env   # then put your token in .env
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. Open **http://localhost:3000** → upload a PDF → ask questions.

## Config (backend `.env`)

| Variable | Required | Description |
|----------|----------|-------------|
| `HUGGINGFACEHUB_API_TOKEN` | Yes | From [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) |
| `EMBEDDING_MODEL` | No | Default: `sentence-transformers/all-MiniLM-L6-v2` |
| `CHAT_MODEL` | No | Default: `HuggingFaceH4/zephyr-7b-beta` |

That’s it. No Ollama, no OpenAI, no other keys.
