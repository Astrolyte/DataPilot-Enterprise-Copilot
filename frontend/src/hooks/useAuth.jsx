import { createContext, useContext, useMemo, useState } from 'react'
import { clearSession, getSession, saveSession } from '../lib/storage'
import { login } from '../lib/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [session, setSession] = useState(getSession)

  const signIn = async (username, password) => {
    const data = await login(username, password)
    const next = {
      token: data.access_token,
      user: data.user,
    }
    saveSession(next)
    setSession(next)
    return next
  }

  const signOut = () => {
    clearSession()
    setSession(null)
  }

  const value = useMemo(() => ({
    session,
    user: session?.user || null,
    token: session?.token || null,
    signIn,
    signOut,
  }), [session])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  return useContext(AuthContext)
}