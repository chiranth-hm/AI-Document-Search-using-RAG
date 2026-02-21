export function Header() {
  return (
    <header className="border-b border-surface-lighter/50 bg-surface/80 backdrop-blur-sm sticky top-0 z-10">
      <div className="max-w-4xl mx-auto px-4 py-4">
        <h1 className="text-xl font-semibold text-white tracking-tight">
          AI Document Search
        </h1>
        <p className="text-sm text-slate-400 mt-0.5">
          Chat with PDFs using LLM + semantic search
        </p>
      </div>
    </header>
  )
}
