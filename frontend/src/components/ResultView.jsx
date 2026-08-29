import { Braces, Check, Clock3, Copy, Database, FileText, Table2 } from 'lucide-react'
import { useState } from 'react'
import RouteBadge from './RouteBadge'

function Source({ source }) {
  const name = source?.document_id || source?.name || source?.title || 'Source document'
  const type = source?.type || source?.category || 'Document'
  return (
    <div className="flex items-center gap-3 rounded-xl border border-[#e7e5e1] bg-white px-3.5 py-3">
      <div className="grid h-8 w-8 shrink-0 place-items-center rounded-lg bg-[#f2f1ee] text-zinc-500"><FileText size={15} /></div>
      <div className="min-w-0">
        <div className="truncate text-[12px] font-medium text-zinc-800">{name}</div>
        <div className="mt-0.5 text-[10px] uppercase tracking-wider text-zinc-400">{type}</div>
      </div>
    </div>
  )
}

export default function ResultView({ result, duration }) {
  const [copied, setCopied] = useState(false)
  if (!result) return null

  const copy = async () => {
    const text = result.answer || result.sql || JSON.stringify(result.rows || [], null, 2)
    await navigator.clipboard?.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 1200)
  }

  const rows = Array.isArray(result.rows) ? result.rows : []
  const sources = Array.isArray(result.sources) ? result.sources : []

  return (
    <div className="fade-up mt-7 space-y-5">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <RouteBadge route={result.route} />
          {duration != null && <span className="flex items-center gap-1 text-[11px] text-zinc-400"><Clock3 size={12} /> {duration} ms</span>}
        </div>
        <button onClick={copy} className="flex items-center gap-1.5 rounded-lg px-2.5 py-1.5 text-[11px] font-medium text-zinc-500 hover:bg-zinc-100">
          {copied ? <Check size={13} /> : <Copy size={13} />} {copied ? 'Copied' : 'Copy'}
        </button>
      </div>

      {result.answer && (
        <section className="panel soft-shadow rounded-2xl p-5 md:p-6">
          <div className="mb-3 text-[10px] font-semibold uppercase tracking-[0.16em] text-zinc-400">Answer</div>
          <div className="whitespace-pre-wrap text-[15px] leading-7 text-zinc-800">{result.answer}</div>
        </section>
      )}

      {result.sql && (
        <section className="overflow-hidden rounded-2xl border border-[#2b2930] bg-[#242229]">
          <div className="flex items-center justify-between border-b border-white/10 px-4 py-3">
            <div className="flex items-center gap-2 text-[11px] font-medium text-zinc-300"><Database size={14} /> Generated SQL</div>
            <span className="text-[10px] uppercase tracking-wider text-zinc-500">read-only</span>
          </div>
          <pre className="overflow-x-auto p-4 text-[12px] leading-6 text-zinc-200">{result.sql}</pre>
        </section>
      )}

      {rows.length > 0 && (
        <section className="panel overflow-hidden rounded-2xl">
          <div className="flex items-center gap-2 border-b border-[#e7e5e1] px-4 py-3 text-[11px] font-medium text-zinc-600"><Table2 size={14} /> Results</div>
          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-[12px]">
              <thead className="bg-[#fafaf8] text-[10px] uppercase tracking-wider text-zinc-400">
                <tr>{Object.keys(rows[0]).map(k => <th key={k} className="whitespace-nowrap px-4 py-3 font-semibold">{k}</th>)}</tr>
              </thead>
              <tbody>{rows.map((row, i) => (
                <tr key={i} className="border-t border-[#eee]">
                  {Object.keys(rows[0]).map(k => <td key={k} className="whitespace-nowrap px-4 py-3 text-zinc-700">{String(row[k] ?? '—')}</td>)}
                </tr>
              ))}</tbody>
            </table>
          </div>
        </section>
      )}

      {sources.length > 0 && (
        <section>
          <div className="mb-2.5 flex items-center gap-2 text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-400"><Braces size={13} /> Sources</div>
          <div className="grid gap-2 sm:grid-cols-2">{sources.map((s, i) => <Source key={i} source={s} />)}</div>
        </section>
      )}
    </div>
  )
}