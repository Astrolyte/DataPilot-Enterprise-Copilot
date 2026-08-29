import { Shield, Server, UserRound } from 'lucide-react'
import { useAuth } from '../hooks/useAuth.jsx'
import { API_BASE } from '../lib/api'

export default function Settings() {
  const { user } = useAuth()
  return (
    <div className="mx-auto max-w-[760px] px-5 py-8 md:px-10 md:py-12">
      <div><div className="mb-2 text-[11px] font-semibold uppercase tracking-[0.15em] text-[#7569a4]">Workspace</div><h1 className="text-[29px] font-semibold tracking-[-0.045em]">Settings</h1><p className="mt-2 text-[13px] text-zinc-500">Account and connection details.</p></div>
      <div className="mt-8 space-y-3">
        <section className="panel rounded-2xl p-5">
          <div className="flex items-center gap-3"><div className="grid h-9 w-9 place-items-center rounded-lg bg-[#f1eefb] text-[#675b96]"><UserRound size={16}/></div><div><h2 className="text-[13px] font-semibold">Account</h2><p className="text-[11px] text-zinc-400">Authenticated DataPilot identity</p></div></div>
          <div className="mt-5 grid gap-4 sm:grid-cols-2"><div><div className="text-[10px] uppercase tracking-wider text-zinc-400">Name</div><div className="mt-1 text-[13px] text-zinc-700">{user?.username || '—'}</div></div><div><div className="text-[10px] uppercase tracking-wider text-zinc-400">Email</div><div className="mt-1 text-[13px] text-zinc-700">{user?.email || '—'}</div></div><div><div className="text-[10px] uppercase tracking-wider text-zinc-400">Role</div><div className="mt-1 text-[13px] text-zinc-700">{user?.role || '—'}</div></div></div>
        </section>
        <section className="panel rounded-2xl p-5">
          <div className="flex items-center gap-3"><div className="grid h-9 w-9 place-items-center rounded-lg bg-[#f2f1ee] text-zinc-600"><Server size={16}/></div><div><h2 className="text-[13px] font-semibold">API connection</h2><p className="text-[11px] text-zinc-400">Current frontend backend target</p></div></div>
          <div className="mt-5 rounded-xl bg-[#fafaf8] px-3.5 py-3 font-mono text-[11px] text-zinc-600 break-all">{API_BASE}</div>
        </section>
        <section className="panel rounded-2xl p-5">
          <div className="flex items-center gap-3"><div className="grid h-9 w-9 place-items-center rounded-lg bg-[#edf6ef] text-[#356544]"><Shield size={16}/></div><div><h2 className="text-[13px] font-semibold">Security</h2><p className="text-[11px] text-zinc-400">Access is controlled by your backend session.</p></div></div>
          <p className="mt-4 text-[12px] leading-5 text-zinc-500">DataPilot uses bearer-token authentication for protected query requests. Keep your API environment private and configure a production HTTPS endpoint before deployment.</p>
        </section>
      </div>
    </div>
  )
}