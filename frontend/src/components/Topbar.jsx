import { Menu } from 'lucide-react'
import Logo from './Logo'
import { useAuth } from '../hooks/useAuth.jsx'

export default function Topbar({ onMenu }) {
  const { user } = useAuth()
  return (
    <header className="flex h-17 items-center justify-between border-b border-[#e7e5e1] bg-[#fafaf8] px-5 md:hidden">
      <button onClick={onMenu} className="rounded-lg p-2 text-zinc-600 hover:bg-zinc-100"><Menu size={20} /></button>
      <Logo compact />
      <div className="grid h-8 w-8 place-items-center rounded-full bg-[#e9e6f7] text-xs font-semibold text-[#554b83]">
        {(user?.username || 'U').slice(0, 1).toUpperCase()}
      </div>
    </header>
  )
}