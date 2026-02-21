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

3. **Frontend** (with Firebase login)
   - In Firebase Console, enable **Email/Password** and **Google** under Authentication → Sign-in method.
   - Create a Web app if needed; copy the config into `frontend/.env` (see `frontend/.env.example`). Use your project ID (e.g. `document-search-using-rag`) and fill `VITE_FIREBASE_API_KEY`, `VITE_FIREBASE_APP_ID`, `VITE_FIREBASE_MESSAGING_SENDER_ID` from the Firebase config.
   ```bash
   cd frontend
   npm install
   cp .env.example .env   # then add your Firebase config values
   npm run dev
   ```

4. Open **http://localhost:3000** → sign in or sign up (separate page) → then upload a PDF and ask questions.

## Config (backend `.env`)

| Variable | Required | Description |
|----------|----------|-------------|
| `HUGGINGFACEHUB_API_TOKEN` | Yes | From [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) |
| `EMBEDDING_MODEL` | No | Default: `sentence-transformers/all-MiniLM-L6-v2` |
| `CHAT_MODEL` | No | Default: `HuggingFaceH4/zephyr-7b-beta` |

## Firebase (frontend `frontend/.env`)

| Variable | Description |
|----------|-------------|
| `VITE_FIREBASE_API_KEY` | From Firebase Console → Project settings → Your apps |
| `VITE_FIREBASE_AUTH_DOMAIN` | e.g. `document-search-using-rag.firebaseapp.com` |
| `VITE_FIREBASE_PROJECT_ID` | e.g. `document-search-using-rag` |
| `VITE_FIREBASE_STORAGE_BUCKET` | e.g. `document-search-using-rag.firebasestorage.app` |
| `VITE_FIREBASE_MESSAGING_SENDER_ID` | From Firebase config |
| `VITE_FIREBASE_APP_ID` | From Firebase config |

Login/sign-up page is at **/login**; the main app is protected and requires sign-in (Email/Password or Google).
