import { useState } from 'react'

export function MessageBubble({ message }) {
  const [sourcesOpen, setSourcesOpen] = useState(false)
  const isUser = message.role === 'user'
  const sources = message.sources || []

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[85%] rounded-2xl px-4 py-2.5 ${
          isUser
            ? 'bg-brand-600 text-white'
            : message.error
              ? 'bg-red-500/20 text-red-300'
              : 'bg-surface-light text-slate-200'
        }`}
      >
        <div className="whitespace-pre-wrap break-words">{message.content}</div>
        {!isUser && sources.length > 0 && (
          <div className="mt-3 pt-3 border-t border-surface-lighter/50">
            <button
              type="button"
              onClick={() => setSourcesOpen((o) => !o)}
              className="text-xs text-brand-400 hover:text-brand-300"
            >
              {sourcesOpen ? 'Hide sources' : 'View sources'}
            </button>
            {sourcesOpen && (
              <ul className="mt-2 space-y-2 text-xs text-slate-400">
                {sources.map((s, i) => (
                  <li
                    key={i}
                    className="pl-2 border-l-2 border-surface-lighter truncate max-h-20 overflow-y-auto"
                  >
                    {s.content?.slice(0, 300)}
                    {(s.content?.length || 0) > 300 && '…'}
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
