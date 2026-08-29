import { useState } from 'react'
import { ArrowUpRight, Clock3, Search, Trash2 } from 'lucide-react'
import { getHistory, clearHistory } from '../lib/storage'
import RouteBadge from '../components/RouteBadge'

export default function History() {
  const [items, setItems] = useState(getHistory)
  const [search, setSearch] = useState('')
  const filtered = items.filter(x => x.question.toLowerCase().includes(search.toLowerCase()))

  const clear = () => { clearHistory(); setItems([]) }

  return (
    <div className="mx-auto max-w-[980px] px-5 py-8 md:px-10 md:py-12">
      <div className="flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
        <div><div className="mb-2 text-[11px] font-semibold uppercase tracking-[0.15em] text-[#7569a4]">Workspace</div><h1 className="text-[29px] font-semibold tracking-[-0.045em]">Query history</h1><p className="mt-2 text-[13px] text-zinc-500">Questions asked from this browser.</p></div>
        {items.length > 0 && <button onClick={clear} className="flex items-center gap-2 self-start rounded-lg px-2.5 py-2 text-[11px] font-medium text-zinc-500 hover:bg-zinc-100"><Trash2 size={14} /> Clear history</button>}
      </div>

      <div className="relative mt-8">
        <Search size={15} className="absolute left-3.5 top-3.5 text-zinc-400" />
        <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search questions…" className="h-11 w-full rounded-xl border border-[#dedcd8] bg-white pl-10 pr-4 text-[13px] outline-none focus:border-[#8c80c4] focus:ring-4 focus:ring-[#8c80c4]/10" />
      </div>

      <div className="mt-4 overflow-hidden rounded-2xl border border-[#e7e5e1] bg-white">
        {filtered.length ? filtered.map(item => (
          <div key={item.id} className="border-b border-[#eee] p-4 last:border-0 md:px-5">
            <div className="flex items-start justify-between gap-4">
              <div className="min-w-0"><div className="text-[13px] font-medium leading-5 text-zinc-800">{item.question}</div><div className="mt-2 flex flex-wrap items-center gap-2"><RouteBadge route={item.route} /><span className="flex items-center gap-1 text-[10px] text-zinc-400"><Clock3 size={11}/>{item.duration ?? '—'} ms</span><span className="text-[10px] text-zinc-400">{new Date(item.createdAt).toLocaleString()}</span></div></div>
              <ArrowUpRight size={16} className="shrink-0 text-zinc-300" />
            </div>
          </div>
        )) : <div className="px-5 py-14 text-center text-[12px] text-zinc-400">No queries found.</div>}
      </div>
    </div>
  )
}