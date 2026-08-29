import { useEffect, useState } from "react";
import { Eye, EyeOff, LockKeyhole, Mail, ArrowRight, User } from "lucide-react";
import { useNavigate, Link } from "react-router-dom";
import { API_BASE } from "../lib/api";
import { useAuth } from "../hooks/useAuth.jsx";
import { saveSession } from "../lib/storage";
import Logo from "../components/Logo";

export default function Register() {
  const { session } = useAuth();
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [show, setShow] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (session) navigate("/", { replace: true });
  }, [session, navigate]);

  const submit = async (e) => {
    e.preventDefault();
    setError("");

    if (!name.trim()) {
      setError("Name is required");
      return;
    }
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }
    if (password.length < 8) {
      setError("Password must be at least 8 characters long");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email,
          name,
          password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Registration failed");
      }

      // Save session data using the correct storage function
      saveSession({
        token: data.access_token,
        user: data.user,
      });

      // Reload to update auth context
      setTimeout(() => (window.location.href = "/"), 500);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid min-h-screen place-items-center px-5 py-10">
      <div className="w-full max-w-[410px]">
        <div className="mb-10 flex justify-center">
          <Logo />
        </div>
        <div className="panel soft-shadow rounded-2xl p-7 md:p-8">
          <div className="mb-7">
            <h1 className="text-[24px] font-semibold tracking-[-0.035em] text-zinc-900">
              Create account
            </h1>
            <p className="mt-2 text-[13px] leading-5 text-zinc-500">
              Sign up to get started with DataPilot.
            </p>
          </div>

          <form onSubmit={submit} className="space-y-4">
            <label className="block">
              <span className="mb-1.5 block text-[11px] font-semibold uppercase tracking-[0.12em] text-zinc-500">
                Full Name
              </span>
              <div className="relative">
                <User
                  className="absolute left-3.5 top-3.5 text-zinc-400"
                  size={16}
                />
                <input
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  type="text"
                  required
                  placeholder="John Doe"
                  className="h-11 w-full rounded-xl border border-[#dedcd8] bg-white pl-10 pr-3 text-[13px] outline-none transition placeholder:text-zinc-300 focus:border-[#8c80c4] focus:ring-4 focus:ring-[#8c80c4]/10"
                />
              </div>
            </label>

            <label className="block">
              <span className="mb-1.5 block text-[11px] font-semibold uppercase tracking-[0.12em] text-zinc-500">
                Email
              </span>
              <div className="relative">
                <Mail
                  className="absolute left-3.5 top-3.5 text-zinc-400"
                  size={16}
                />
                <input
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  type="email"
                  required
                  autoComplete="email"
                  placeholder="you@company.com"
                  className="h-11 w-full rounded-xl border border-[#dedcd8] bg-white pl-10 pr-3 text-[13px] outline-none transition placeholder:text-zinc-300 focus:border-[#8c80c4] focus:ring-4 focus:ring-[#8c80c4]/10"
                />
              </div>
            </label>

            <label className="block">
              <span className="mb-1.5 block text-[11px] font-semibold uppercase tracking-[0.12em] text-zinc-500">
                Password
              </span>
              <div className="relative">
                <LockKeyhole
                  className="absolute left-3.5 top-3.5 text-zinc-400"
                  size={16}
                />
                <input
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  type={show ? "text" : "password"}
                  required
                  autoComplete="new-password"
                  placeholder="••••••••"
                  className="h-11 w-full rounded-xl border border-[#dedcd8] bg-white pl-10 pr-11 text-[13px] outline-none transition placeholder:text-zinc-300 focus:border-[#8c80c4] focus:ring-4 focus:ring-[#8c80c4]/10"
                />
                <button
                  type="button"
                  onClick={() => setShow(!show)}
                  className="absolute right-2.5 top-2.5 rounded-lg p-1.5 text-zinc-400 hover:bg-zinc-100"
                >
                  {show ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </label>

            <label className="block">
              <span className="mb-1.5 block text-[11px] font-semibold uppercase tracking-[0.12em] text-zinc-500">
                Confirm Password
              </span>
              <div className="relative">
                <LockKeyhole
                  className="absolute left-3.5 top-3.5 text-zinc-400"
                  size={16}
                />
                <input
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  type={showConfirm ? "text" : "password"}
                  required
                  autoComplete="new-password"
                  placeholder="••••••••"
                  className="h-11 w-full rounded-xl border border-[#dedcd8] bg-white pl-10 pr-11 text-[13px] outline-none transition placeholder:text-zinc-300 focus:border-[#8c80c4] focus:ring-4 focus:ring-[#8c80c4]/10"
                />
                <button
                  type="button"
                  onClick={() => setShowConfirm(!showConfirm)}
                  className="absolute right-2.5 top-2.5 rounded-lg p-1.5 text-zinc-400 hover:bg-zinc-100"
                >
                  {showConfirm ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </label>

            {error && (
              <div className="rounded-xl border border-red-200 bg-red-50 px-3.5 py-2.5 text-[12px] leading-5 text-red-700">
                {error}
              </div>
            )}

            <button
              disabled={loading}
              className="flex h-11 w-full items-center justify-center gap-2 rounded-xl bg-[#292530] text-[13px] font-semibold text-white transition hover:bg-[#201d25] disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? (
                "Creating account…"
              ) : (
                <>
                  Sign up <ArrowRight size={15} />
                </>
              )}
            </button>
          </form>

          <div className="mt-6 text-center text-[13px] text-zinc-600">
            Already have an account?{" "}
            <Link
              to="/login"
              className="font-semibold text-[#8c80c4] hover:underline"
            >
              Sign in
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
