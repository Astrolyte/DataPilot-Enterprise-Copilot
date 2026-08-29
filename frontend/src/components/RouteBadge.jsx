const styles = {
  SQL: 'bg-[#edf6ef] text-[#356544] border-[#dcecdf]',
  RAG: 'bg-[#f1eefb] text-[#5b4d8e] border-[#e4def6]',
  HYBRID: 'bg-[#f8f1e7] text-[#7a5a2d] border-[#eee1cd]',
}

export default function RouteBadge({ route }) {
  return <span className={`inline-flex rounded-full border px-2 py-0.5 text-[10px] font-semibold tracking-[0.08em] ${styles[route] || 'bg-zinc-100 text-zinc-600 border-zinc-200'}`}>{route}</span>
}