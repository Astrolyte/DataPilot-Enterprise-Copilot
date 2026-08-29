import { NavLink } from 'react-router-dom'
import { BarChart3, Clock3, FileSearch, LogOut, Settings, Sparkles, X } from 'lucide-react'
import Logo from './Logo'
import { useAuth } from '../hooks/useAuth.jsx'

const items = [
  { to: '/', label: 'Ask Data', icon: Sparkles, end: true },
  { to: '/history', label: 'History', icon: Clock3 },
  { to: '/audit', label: 'Audit logs', icon: FileSearch },
]

export default function Sidebar({ open, onClose }) {
  const { user, signOut } = useAuth()
  return (
    <>
      {open && <button onClick={onClose} className="fixed inset-0 z-40 bg-black/20 md:hidden" aria-label="Close menu" />}
      <aside className={`fixed inset-y-0 left-0 z-50 flex w-63 flex-col border-r border-[#e7e5e1] bg-[#fafaf8] px-4 py-5 transition-transform duration-200 md:static md:translate-x-0 ${open ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="flex items-center justify-between px-2">
          <Logo />
          <button onClick={onClose} className="rounded-lg p-2 text-zinc-400 hover:bg-zinc-100 md:hidden"><X size={18} /></button>
        </div>

        <nav className="mt-9 space-y-1">
          {items.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              onClick={onClose}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-[10px] px-3 py-2.5 text-[13px] font-medium transition ${
                  isActive ? 'bg-[#efedf8] text-[#51468b]' : 'text-zinc-600 hover:bg-zinc-100 hover:text-zinc-900'
                }`
              }
            >
              <Icon size={17} strokeWidth={1.8} />
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="mt-auto">
          <div className="mb-3 rounded-xl border border-[#e7e5e1] bg-white p-3">
            <div className="flex items-center gap-2.5">
              <div className="grid h-8 w-8 place-items-center rounded-full bg-[#e9e6f7] text-xs font-semibold text-[#554b83]">
                {(user?.username || user?.email || 'U').slice(0, 1).toUpperCase()}
              </div>
              <div className="min-w-0">
                <div className="truncate text-[12px] font-semibold text-zinc-800">{user?.username || 'User'}</div>
                <div className="truncate text-[11px] text-zinc-400">{user?.role || 'User'}</div>
              </div>
            </div>
          </div>
          <NavLink to="/settings" onClick={onClose} className="flex items-center gap-3 rounded-[10px] px-3 py-2.5 text-[13px] text-zinc-600 hover:bg-zinc-100">
            <Settings size={17} strokeWidth={1.8} /> Settings
          </NavLink>
          <button onClick={signOut} className="mt-1 flex w-full items-center gap-3 rounded-[10px] px-3 py-2.5 text-[13px] text-zinc-500 hover:bg-zinc-100 hover:text-zinc-900">
            <LogOut size={17} strokeWidth={1.8} /> Sign out
          </button>
        </div>
      </aside>
    </>
  )
}