import { signOut } from 'firebase/auth'
import { auth } from '../firebase'

export function Header() {
  const user = auth.currentUser

  const handleLogout = () => {
    signOut(auth)
  }

  return (
    <header className="border-b border-surface-lighter/50 bg-surface/80 backdrop-blur-sm sticky top-0 z-10">
      <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-semibold text-white tracking-tight">
            Document Search using RAG
          </h1>
          <p className="text-sm text-slate-400 mt-0.5">
            Chat with PDFs using LLM + semantic search
          </p>
        </div>
        {user && (
          <div className="flex items-center gap-3 shrink-0">
            <span className="text-slate-400 text-sm truncate max-w-[160px]" title={user.email}>
              {user.email}
            </span>
            <button
              type="button"
              onClick={handleLogout}
              className="px-3 py-1.5 rounded-lg text-sm text-slate-300 hover:bg-surface-lighter hover:text-white transition-colors"
            >
              Log out
            </button>
          </div>
        )}
      </div>
    </header>
  )
}
