export function UploadArea({ onUpload, loading, success, error, fileInputRef, onClearFeedback }) {
  const handleChange = (e) => {
    const files = e.target.files
    if (files?.length) onUpload(Array.from(files))
    e.target.value = ''
  }

  return (
    <section className="mb-6">
      <div
        className="border border-dashed border-surface-lighter rounded-xl p-6 text-center transition-colors hover:border-brand-500/50"
        onClick={() => fileInputRef.current?.click()}
        onKeyDown={(e) => e.key === 'Enter' && fileInputRef.current?.click()}
        role="button"
        tabIndex={0}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          multiple
          className="hidden"
          onChange={handleChange}
          disabled={loading}
        />
        {loading ? (
          <p className="text-brand-400">Ingesting PDFs… (first time or large file may take 1–2 min)</p>
        ) : (
          <>
            <p className="text-slate-300">Drop PDFs here or click to upload</p>
            <p className="text-slate-500 text-sm mt-1">Max 10MB per file</p>
          </>
        )}
      </div>
      {success && (
        <div
          className="mt-3 px-4 py-2 rounded-lg bg-emerald-500/20 text-emerald-300 text-sm flex justify-between items-center"
          role="status"
        >
          <span>{success}</span>
          <button
            type="button"
            onClick={onClearFeedback}
            className="text-emerald-400 hover:text-emerald-200"
            aria-label="Dismiss"
          >
            ×
          </button>
        </div>
      )}
      {error && (
        <div
          className="mt-3 px-4 py-2 rounded-lg bg-red-500/20 text-red-300 text-sm flex justify-between items-center"
          role="alert"
        >
          <span>{error}</span>
          <button
            type="button"
            onClick={onClearFeedback}
            className="text-red-400 hover:text-red-200"
            aria-label="Dismiss"
          >
            ×
          </button>
        </div>
      )}
    </section>
  )
}
