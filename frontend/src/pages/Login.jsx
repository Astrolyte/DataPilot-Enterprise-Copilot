import { useEffect, useState } from "react";
import { Eye, EyeOff, LockKeyhole, Mail, ArrowRight } from "lucide-react";
import { useLocation, useNavigate, Link } from "react-router-dom";
import { googleLoginUrl } from "../lib/api";
import { useAuth } from "../hooks/useAuth.jsx";
import Logo from "../components/Logo";

export default function Login() {
  const { session, signIn } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [show, setShow] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (session) navigate("/", { replace: true });
  }, [session, navigate]);

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await signIn(email, password);
      navigate(location.state?.from || "/", { replace: true });
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
              Welcome back
            </h1>
            <p className="mt-2 text-[13px] leading-5 text-zinc-500">
              Sign in to your DataPilot workspace.
            </p>
          </div>

          <form onSubmit={submit} className="space-y-4">
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
                  autoComplete="current-password"
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
                "Signing in…"
              ) : (
                <>
                  Sign in <ArrowRight size={15} />
                </>
              )}
            </button>
          </form>

          <div className="my-6 flex items-center gap-3">
            <div className="h-px flex-1 bg-[#e7e5e1]" />
            <span className="text-[10px] uppercase tracking-[0.14em] text-zinc-400">
              or
            </span>
            <div className="h-px flex-1 bg-[#e7e5e1]" />
          </div>

          <a
            href={googleLoginUrl()}
            className="flex h-11 w-full items-center justify-center gap-2.5 rounded-xl border border-[#dedcd8] bg-white text-[13px] font-medium text-zinc-700 transition hover:bg-zinc-50"
          >
            <span className="grid h-5 w-5 place-items-center rounded-full border border-zinc-200 text-[11px] font-semibold">
              G
            </span>
            Continue with Google
          </a>

          <div className="mt-6 text-center text-[13px] text-zinc-600">
            Don't have an account?{" "}
            <Link
              to="/register"
              className="font-semibold text-[#8c80c4] hover:underline"
            >
              Sign up
            </Link>
          </div>
        </div>

        <p className="mt-5 text-center text-[10px] leading-5 text-zinc-400">
          Authorized employees only · DataPilot access is monitored.
        </p>
      </div>
    </div>
  );
}
