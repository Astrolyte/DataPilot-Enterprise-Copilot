import { useState } from 'react'
import { ShieldCheck, Info } from 'lucide-react'

const demo = [
  { id: 'e8fc1a05', query: 'What is the refund policy?', route: 'RAG', tables: '—', sources: 'refund_policy, contract_913', latency: 2630, status: 'SUCCESS', time: 'Today' },
]

export default function AuditLogs() {
  const [logs] = useState(demo)
  return (
    <div className="mx-auto max-w-[1100px] px-5 py-8 md:px-10 md:py-12">
      <div><div className="mb-2 text-[11px] font-semibold uppercase tracking-[0.15em] text-[#7569a4]">Governance</div><h1 className="text-[29px] font-semibold tracking-[-0.045em]">Audit logs</h1><p className="mt-2 max-w-[650px] text-[13px] leading-6 text-zinc-500">A record of query routing, latency, data sources, and execution status.</p></div>
      <div className="mt-7 flex items-start gap-3 rounded-xl border border-[#e7e5e1] bg-white px-4 py-3.5 text-[11px] leading-5 text-zinc-500"><Info size={15} className="mt-0.5 shrink-0 text-[#7569a4]" /> The audit table is populated by the backend. This view is ready for a GET audit endpoint when you expose one.</div>
      <div className="mt-5 overflow-x-auto rounded-2xl border border-[#e7e5e1] bg-white">
        <table className="min-w-[900px] w-full text-left text-[11px]">
          <thead className="bg-[#fafaf8] text-[9px] uppercase tracking-[0.14em] text-zinc-400"><tr>{['Request','Query','Route','Tables','Sources','Latency','Status'].map(x => <th key={x} className="px-4 py-3.5 font-semibold">{x}</th>)}</tr></thead>
          <tbody>{logs.map(log => <tr key={log.id} className="border-t border-[#eee] align-top">
            <td className="px-4 py-4 font-mono text-zinc-400">{log.id}…</td><td className="max-w-[280px] px-4 py-4 font-medium text-zinc-700">{log.query}</td><td className="px-4 py-4 font-semibold text-[#62568d]">{log.route}</td><td className="px-4 py-4 text-zinc-500">{log.tables}</td><td className="max-w-[220px] px-4 py-4 text-zinc-500">{log.sources}</td><td className="px-4 py-4 text-zinc-500">{log.latency} ms</td><td className="px-4 py-4"><span className="inline-flex items-center gap-1 rounded-full bg-[#edf6ef] px-2 py-1 text-[9px] font-semibold text-[#356544]"><ShieldCheck size={11}/>{log.status}</span></td>
          </tr>)}</tbody>
        </table>
      </div>
    </div>
  )
}