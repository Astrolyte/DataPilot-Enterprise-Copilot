export default function Logo({ compact = false }) {
  return (
    <div className="flex items-center gap-2.5">
      <div className="grid h-8 w-8 place-items-center rounded-[10px] bg-[#25212f] text-white shadow-sm">
        <span className="text-sm font-semibold tracking-tight">D</span>
      </div>
      {!compact && (
        <div className="leading-none">
          <div className="text-[15px] font-semibold tracking-[-0.02em]">DataPilot</div>
          <div className="mt-1 text-[9px] font-medium uppercase tracking-[0.18em] text-zinc-400">Enterprise Copilot</div>
        </div>
      )}
    </div>
  )
}