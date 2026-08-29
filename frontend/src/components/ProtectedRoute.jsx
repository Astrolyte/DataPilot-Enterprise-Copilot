import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth.jsx'

export default function ProtectedRoute() {
  const { session } = useAuth()
  const location = useLocation()
  if (!session?.token) return <Navigate to="/login" replace state={{ from: location.pathname }} />
  return <Outlet />
}