'use client'

import { useState } from 'react'
import { Upload, Bug, AlertCircle, CheckCircle2, Loader2, Sparkles } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

export default function Home() {
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<any[]>([])
  const [error, setError] = useState<string | null>(null)

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setLoading(true)
    setError(null)
    
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('/api/process', {
        method: 'POST',
        body: formData,
      })
      
      if (!response.ok) throw new Error('Failed to process file')
      
      const data = await response.json()
      setResults(data.results)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="app-container">
      <header className="animate-fade" style={{ animationDelay: '0.1s' }}>
        <div className="bug-id" style={{ color: 'var(--primary)', marginBottom: '1rem' }}>
          <Sparkles size={16} className="inline mr-2" />
          Agentic AI Pipeline Loaded
        </div>
        <h1>Bug Hunter Pro</h1>
        <p className="subtitle">
          Advanced 3-agent orchestration for mission-critical RDI code analysis.
        </p>
      </header>

      <section className="animate-fade" style={{ animationDelay: '0.2s' }}>
        {!results.length && !loading && (
          <div className="glass-card">
            <label className="upload-area">
              <input type="file" className="hidden" onChange={handleFileUpload} accept=".csv" />
              <div className="flex flex-col items-center">
                <div className="upload-icon-container">
                  <Upload size={32} color="var(--primary)" />
                </div>
                <div className="mb-6">
                  <h3 className="text-2xl font-bold mb-2 tracking-tight">Upload Pipeline Data</h3>
                  <p className="text-slate-400">Drag and drop or select your `samples.csv` file</p>
                </div>
                <span className="btn-primary">Browse Files</span>
              </div>
            </label>
          </div>
        )}

        {loading && (
          <div className="glass-card flex flex-col items-center justify-center py-20 gap-6">
            <Loader2 size={48} className="animate-spin text-emerald-500" />
            <div className="text-center">
              <h3 className="text-xl font-semibold">Running Multi-Agent Pipeline</h3>
              <p className="text-gray-400 mt-2">Connecting to MCP Server & Gemini 2.0 Flash...</p>
            </div>
            <div className="w-full max-w-sm h-1 bg-gray-800 rounded-full overflow-hidden mt-4">
              <motion.div 
                className="h-full bg-emerald-500"
                initial={{ width: 0 }}
                animate={{ width: '100%' }}
                transition={{ duration: 15, ease: "linear" }}
              />
            </div>
          </div>
        )}

        {error && (
          <div className="glass-card border-rose-500/50 bg-rose-500/5 p-6 flex items-center gap-4 text-rose-400">
            <AlertCircle size={24} />
            <p>{error}</p>
          </div>
        )}

        {results.length > 0 && (
          <div className="dashboard-grid">
            <AnimatePresence>
              {results.map((res, idx) => (
                <motion.div 
                  key={res.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.1 }}
                  className="glass-card bug-card"
                >
                  <div className="flex justify-between items-center">
                    <span className="bug-id">SAMPLE #{res.id}</span>
                    <Bug size={16} className="text-rose-500" />
                  </div>
                  
                  <div className="code-block">
                    {res.code.split('\n').map((line: string, i: number) => {
                      const lineNum = i + 1;
                      const isBuggy = res.bug_line.includes(String(lineNum));
                      return (
                        <div key={i} className={isBuggy ? 'highlight' : ''}>
                          <span style={{ opacity: 0.3, marginRight: '1rem' }}>{lineNum}</span>
                          {line}
                        </div>
                      )
                    })}
                  </div>

                  <div className="flex items-start gap-3 mt-2">
                    <CheckCircle2 size={18} className="text-emerald-500 mt-1 shrink-0" />
                    <p className="explanation">
                      <strong className="text-white">Analysis:</strong> {res.explanation}
                    </p>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        )}
      </section>

      <footer className="mt-20 text-center text-gray-600 text-sm py-10">
        <p>© 2026 Agentic Bug Hunter • Powered by Google DeepMind & OpenRouter</p>
      </footer>
    </main>
  )
}
