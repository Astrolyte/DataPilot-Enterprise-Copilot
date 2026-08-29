import { Routes, Route } from "react-router-dom";
import { useState } from "react";
import { AuthProvider } from "./hooks/useAuth";
import ProtectedRoute from "./components/ProtectedRoute";
import Sidebar from "./components/Sidebar";
import Topbar from "./components/Topbar";
import Login from "./pages/Login";
import Register from "./pages/Register";
import AuthCallback from "./pages/AuthCallback";
import Dashboard from "./pages/Dashboard";
import History from "./pages/History";
import AuditLogs from "./pages/AuditLogs";
import Settings from "./pages/Settings";

function AppLayout() {
  const [open, setOpen] = useState(false);
  return (
    <div className="app-shell md:flex">
      <Sidebar open={open} onClose={() => setOpen(false)} />
      <main className="min-w-0 flex-1">
        <Topbar onMenu={() => setOpen(true)} />
        <Routes>
          <Route
            path="/"
            element={<Dashboard onMenu={() => setOpen(true)} />}
          />
          <Route path="/history" element={<History />} />
          <Route path="/audit" element={<AuditLogs />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </main>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/auth/callback" element={<AuthCallback />} />
        <Route element={<ProtectedRoute />}>
          <Route path="/*" element={<AppLayout />} />
        </Route>
      </Routes>
    </AuthProvider>
  );
}
