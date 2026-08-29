import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { useAuth } from "../hooks/useAuth.jsx";
import { saveSession } from "../lib/storage";

export default function AuthCallback() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { session } = useAuth();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const handleCallback = async () => {
      try {
        const token = searchParams.get("token");
        const email = searchParams.get("email");
        const username = searchParams.get("username");
        const user_id = searchParams.get("user_id");
        const role = searchParams.get("role");

        if (!token) {
          throw new Error("No token received");
        }

        // Save session data using the correct storage function and key
        const sessionData = {
          token,
          user: {
            user_id,
            email,
            username,
            role,
          },
        };
        saveSession(sessionData);

        // Reload page to update auth context
        setTimeout(() => (window.location.href = "/"), 500);
      } catch (err) {
        setError(err.message);
        setLoading(false);
        setTimeout(() => navigate("/login", { replace: true }), 3000);
      }
    };

    if (session) {
      navigate("/", { replace: true });
      return;
    }

    handleCallback();
  }, [searchParams, navigate, session]);

  return (
    <div className="grid min-h-screen place-items-center px-5">
      <div className="text-center">
        {loading ? (
          <>
            <div className="mb-4 h-12 w-12 animate-spin rounded-full border-4 border-[#8c80c4] border-t-[#292530] mx-auto" />
            <p className="text-zinc-600">Completing your sign in...</p>
          </>
        ) : (
          <>
            <p className="text-red-600">{error}</p>
            <p className="mt-2 text-sm text-zinc-500">
              Redirecting to login...
            </p>
          </>
        )}
      </div>
    </div>
  );
}
