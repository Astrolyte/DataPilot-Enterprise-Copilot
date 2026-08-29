import { useEffect, useMemo, useState } from 'react'
import { ArrowUp, BarChart3, ChevronRight, Clock3, Database, Menu, Sparkles } from 'lucide-react'
import { queryData } from '../lib/api'
import { getHistory, saveHistory } from '../lib/storage'
import { useAuth } from '../hooks/useAuth.jsx'
import ResultView from '../components/ResultView'

const suggestions = [
  'How many customers do we have?',
  'What is the refund policy?',
  "What is Price LLC's refund window and how much revenue has Price LLC generated from completed orders?",
]

export default function Dashboard({ onMenu }) {
  const { user, token } = useAuth()
  const [question, setQuestion] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [duration, setDuration] = useState(null)
  const [history, setHistory] = useState(getHistory)

  const greeting = useMemo(() => {
    const h = new Date().getHours()
    return h < 12 ? 'Good morning' : h < 18 ? 'Good afternoon' : 'Good evening'
  }, [])

  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    const tokenFromUrl = params.get('access_token')
    if (tokenFromUrl) window.history.replaceState({}, '', '/')
  }, [])

  const submit = async (e) => {
    e?.preventDefault()
    const q = question.trim()
    if (!q || loading) return
    setLoading(true); setError(''); setResult(null); setDuration(null)
    const start = performance.now()
    try {
      const data = await queryData(q, token)
      const ms = Math.round(performance.now() - start)
      setResult(data); setDuration(ms)
      setHistory(saveHistory({ id: crypto.randomUUID?.() || String(Date.now()), question: q, route: data.route, answer: data.answer, sql: data.sql, sources: data.sources, duration: ms, createdAt: new Date().toISOString() }))
      setQuestion('')
    } catch (err) {
      setError(err.message)
    } finally { setLoading(false) }
  }

  return (
    <div className="min-h-full">
      <div className="mx-auto max-w-[980px] px-5 py-8 md:px-10 md:py-12">
        <div className="mb-9 flex items-start justify-between">
          <div>
            <div className="mb-2 text-[11px] font-semibold uppercase tracking-[0.15em] text-[#7569a4]">{greeting}</div>
            <h1 className="text-[29px] font-semibold tracking-[-0.045em] text-zinc-900 md:text-[34px]">Ask your business data anything.</h1>
            <p className="mt-2 max-w-[610px] text-[13px] leading-6 text-zinc-500">DataPilot routes each question to the right source—structured data, documents, or both.</p>
          </div>
          <button onClick={onMenu} className="rounded-xl border border-[#e2e0dc] bg-white p-2.5 text-zinc-500 md:hidden"><Menu size={18} /></button>
        </div>

        <form onSubmit={submit} className="panel soft-shadow rounded-2xl p-2.5">
          <div className="flex items-end gap-2">
            <textarea value={question} onChange={e => setQuestion(e.target.value)} onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); submit(e) } }}
              rows={2} placeholder="Ask a question about customers, revenue, policies…" className="min-h-[72px] flex-1 resize-none bg-transparent px-3 py-2.5 text-[14px] leading-6 text-zinc-800 outline-none placeholder:text-zinc-400" />
            <button disabled={loading || !question.trim()} className="mb-1 mr-1 grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-[#292530] text-white transition hover:bg-[#201d25] disabled:cursor-not-allowed disabled:opacity-30" aria-label="Ask">
              <ArrowUp size={17} />
            </button>
          </div>
          <div className="flex items-center justify-between border-t border-[#eee] px-3 pt-2">
            <span className="text-[10px] text-zinc-400">{loading ? <span className="dot-pulse">Thinking</span> : 'Enter to send · Shift + Enter for a new line'}</span>
            <span className="flex items-center gap-1.5 text-[10px] text-zinc-400"><Sparkles size={11} /> AI-assisted</span>
          </div>
        </form>

        {!result && !loading && (
          <div className="mt-8">
            <div className="mb-3 text-[10px] font-semibold uppercase tracking-[0.16em] text-zinc-400">Try asking</div>
            <div className="grid gap-2 md:grid-cols-3">
              {suggestions.map(s => (
                <button key={s} onClick={() => setQuestion(s)} className="group rounded-xl border border-[#e7e5e1] bg-white p-3.5 text-left transition hover:-translate-y-0.5 hover:border-[#d8d2eb] hover:shadow-sm">
                  <div className="mb-3 grid h-7 w-7 place-items-center rounded-lg bg-[#f1eefb] text-[#675b96]"><Sparkles size={13} /></div>
                  <div className="text-[12px] font-medium leading-5 text-zinc-700">{s}</div>
                  <ChevronRight className="mt-2 text-zinc-300 transition group-hover:translate-x-0.5 group-hover:text-zinc-500" size={14} />
                </button>
              ))}
            </div>
          </div>
        )}

        {error && <div className="mt-6 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-[12px] leading-5 text-red-700">{error}</div>}

        {loading && (
          <div className="panel mt-7 rounded-2xl p-6">
            <div className="flex items-center gap-3 text-[13px] text-zinc-500"><span className="h-2 w-2 animate-pulse rounded-full bg-[#7569a4]" /> DataPilot is analyzing your question…</div>
            <div className="mt-5 h-2 w-2/3 animate-pulse rounded-full bg-zinc-100" />
            <div className="mt-2 h-2 w-1/2 animate-pulse rounded-full bg-zinc-100" />
          </div>
        )}

        <ResultView result={result} duration={duration} />

        {!result && !loading && history.length > 0 && (
          <div className="mt-10">
            <div className="mb-3 flex items-center justify-between">
              <div className="text-[10px] font-semibold uppercase tracking-[0.16em] text-zinc-400">Recent queries</div>
              <a href="/history" className="text-[11px] font-medium text-[#6b5e98] hover:underline">View all</a>
            </div>
            <div className="divide-y divide-[#eee] rounded-2xl border border-[#e7e5e1] bg-white">
              {history.slice(0, 4).map(item => (
                <button key={item.id} onClick={() => setQuestion(item.question)} className="flex w-full items-center justify-between gap-4 px-4 py-3.5 text-left hover:bg-[#fafaf8]">
                  <div className="min-w-0"><div className="truncate text-[12px] font-medium text-zinc-700">{item.question}</div><div className="mt-1 text-[10px] text-zinc-400">{item.route} · {item.duration || '—'} ms</div></div>
                  <Clock3 size={14} className="shrink-0 text-zinc-300" />
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}