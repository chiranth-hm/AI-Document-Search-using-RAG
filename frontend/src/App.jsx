import { useState, useRef } from 'react'
import { ChatPanel } from './components/ChatPanel'
import { UploadArea } from './components/UploadArea'
import { Header } from './components/Header'

const API_BASE = import.meta.env.VITE_API_URL || '/api'
const INGEST_TIMEOUT_MS = 5 * 60 * 1000  // 5 min (first upload can be slow)
const CHAT_TIMEOUT_MS = 2 * 60 * 1000   // 2 min

function fetchWithTimeout(url, options, ms) {
  const ctrl = new AbortController()
  const id = setTimeout(() => ctrl.abort(), ms)
  return fetch(url, { ...options, signal: ctrl.signal }).finally(() => clearTimeout(id))
}

export default function App() {
  const [messages, setMessages] = useState([])
  const [uploadSuccess, setUploadSuccess] = useState(null)
  const [uploadError, setUploadError] = useState(null)
  const [loading, setLoading] = useState(false)
  const fileInputRef = useRef(null)

  const handleUpload = async (files) => {
    if (!files?.length) return
    setUploadError(null)
    setUploadSuccess(null)
    setLoading(true)
    try {
      let totalChunks = 0
      for (const file of files) {
        const formData = new FormData()
        formData.append('file', file)
        const res = await fetchWithTimeout(`${API_BASE}/ingest`, {
          method: 'POST',
          body: formData,
        }, INGEST_TIMEOUT_MS)
        const data = await res.json()
        if (!res.ok) throw new Error(data.detail || 'Upload failed')
        totalChunks += data.num_chunks || 0
      }
      setUploadSuccess(`Ingested ${files.length} file(s). ${totalChunks} chunks added.`)
    } catch (err) {
      const msg = err.name === 'AbortError' ? 'Upload timed out. Try a smaller PDF or try again.' : (err.message || 'Upload failed')
      setUploadError(msg)
    } finally {
      setLoading(false)
    }
  }

  const sendMessage = async (text) => {
    if (!text.trim()) return
    const userMsg = { role: 'user', content: text }
    setMessages((prev) => [...prev, userMsg])
    setLoading(true)
    try {
      const res = await fetchWithTimeout(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      }, CHAT_TIMEOUT_MS)
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Request failed')
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: data.message,
          sources: data.sources,
        },
      ])
    } catch (err) {
      const msg = err.name === 'AbortError' ? 'Request timed out. Try again.' : err.message
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: `Error: ${msg}`, error: true },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-1 flex flex-col max-w-4xl w-full mx-auto px-4 py-6">
        <UploadArea
          onUpload={handleUpload}
          loading={loading}
          success={uploadSuccess}
          error={uploadError}
          fileInputRef={fileInputRef}
          onClearFeedback={() => {
            setUploadSuccess(null)
            setUploadError(null)
          }}
        />
        <ChatPanel messages={messages} onSend={sendMessage} loading={loading} />
      </main>
    </div>
  )
}
