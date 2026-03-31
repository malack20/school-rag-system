import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { login } from "../services/authService.js";

function GoogleIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 48 48" aria-hidden="true">
      <path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3c-1.6 4.6-6 8-11.3 8-6.9 0-12.5-5.6-12.5-12.5S16.1 11 23 11c3.2 0 6.1 1.2 8.3 3.2l5.7-5.7C33.6 5.7 28.5 4 23 4 10.8 4 1 13.8 1 26s9.8 22 22 22c12.1 0 22-9.8 22-22 0-1.9-.2-3.6-.4-5.5z"/>
      <path fill="#FF3D00" d="M6.3 14.7l6.6 4.9C14.3 16.1 18.4 13 23 13c3.2 0 6.1 1.2 8.3 3.2l5.7-5.7C33.6 5.7 28.5 4 23 4 15.1 4 8.2 8.1 4.4 14l1.9.7z"/>
      <path fill="#4CAF50" d="M23 48c5.5 0 10.6-2.1 14.5-5.6l-6.7-5.5c-2.2 1.5-4.9 2.3-7.8 2.3-5.3 0-9.7-3.4-11.3-8.1l-6.6 5.1C8.9 43.7 15.4 48 23 48z"/>
      <path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-1 2.9-3 5.4-5.7 7.1l6.7 5.5C39.5 43.9 45 36.8 45 26c0-1.9-.2-3.6-.4-5.5z"/>
    </svg>
  );
}

function GitHubIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true">
      <path fill="currentColor" d="M12 .5C5.73.5.76 5.48.76 11.76c0 4.9 3.18 9.05 7.59 10.52.56.1.77-.24.77-.54 0-.27-.01-1.16-.02-2.11-3.09.67-3.75-1.32-3.75-1.32-.51-1.29-1.25-1.64-1.25-1.64-1.02-.7.08-.69.08-.69 1.12.08 1.71 1.15 1.71 1.15 1 .1 1.72-.66 2.04-1.06-.28-.55-.4-1.2-.4-1.86 0-2.66 1.62-3.86 3.53-3.86 1 0 1.86.08 2.11.12.32-.08.98-.14 1.79-.14 2.65 0 3.54 2.04 3.54 3.96 0 .86-.19 1.68-.53 2.42-.2.43-.54.86-.99 1.16.82.75 1.65 2.25 1.65 4.54 0 3.24-.02 5.84-.02 6.63 0 .33.21.66.78.55 4.39-1.49 7.57-5.61 7.57-10.49C23.24 5.48 18.27.5 12 .5Z"/>
    </svg>
  );
}

export default function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [show, setShow] = useState(false);
  const [remember, setRemember] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const onSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await login(email, password);
      if (remember) {
        localStorage.setItem("auth_token", res.token);
      } else {
        sessionStorage.setItem("auth_token", res.token);
      }
      navigate("/chat");
    } catch (err) {
      setError("Incorrect email or password.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen grid md:grid-cols-2">
      <div className="hidden md:flex flex-col justify-center p-12 bg-gradient-to-br from-academic-blue to-academic-cyan text-white relative">
        <div className="absolute inset-0 opacity-10" aria-hidden="true"></div>
        <div className="max-w-md">
          <div className="mb-6">
            <div className="text-2xl font-bold">School AI Assistant</div>
          </div>
          <div className="text-xl font-semibold mb-2">AI-powered helpdesk for students, staff, and visitors.</div>
          <p className="text-white/90">
            This assistant helps you quickly find verified school information including office locations, admission procedures, tendering processes, academic schedules, and institutional guidelines.
          </p>
        </div>
      </div>
      <div className="flex items-center justify-center p-6">
        <div className="w-full max-w-md bg-white rounded-2xl shadow-soft p-6">
          <h1 className="text-2xl font-bold text-gray-900">Welcome Back</h1>
          <p className="text-gray-600 mt-1">Sign in to continue to the School AI Assistant.</p>

          <div className="mt-6 space-y-3">
            <a href="/api/auth/oauth/google" className="flex items-center justify-center gap-3 w-full border rounded-lg py-3 hover:shadow-sm transition">
              <GoogleIcon /> <span className="font-medium">Continue with Google</span>
            </a>
            <a href="/api/auth/oauth/github" className="flex items-center justify-center gap-3 w-full bg-gray-900 text-white rounded-lg py-3 hover:brightness-110 transition">
              <GitHubIcon /> <span className="font-medium">Continue with GitHub</span>
            </a>
          </div>

          <div className="flex items-center my-6">
            <div className="h-px bg-gray-200 flex-1" />
            <div className="px-3 text-gray-500 text-sm">OR</div>
            <div className="h-px bg-gray-200 flex-1" />
          </div>

          {error && <div className="text-sm text-red-600 mb-2" role="alert">{error}</div>}

          <form onSubmit={onSubmit} className="space-y-4" aria-label="Email sign in form">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email Address</label>
              <input
                id="email"
                type="email"
                placeholder="example@student.school.edu"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="mt-1 w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-academic-cyan"
                required
              />
            </div>
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">Password</label>
              <div className="mt-1 relative">
                <input
                  id="password"
                  type={show ? "text" : "password"}
                  placeholder="•••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full border rounded-lg px-3 py-2 pr-10 focus:outline-none focus:ring-2 focus:ring-academic-cyan"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShow(!show)}
                  className="absolute right-2 top-1/2 -translate-y-1/2 text-sm text-gray-500 hover:text-gray-700"
                  aria-label={show ? "Hide password" : "Show password"}
                >
                  {show ? "Hide" : "Show"}
                </button>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <label className="flex items-center gap-2 text-sm">
                <input type="checkbox" checked={remember} onChange={(e) => setRemember(e.target.checked)} />
                Remember me
              </label>
              <a href="#" className="text-sm text-academic-blue hover:underline">Forgot password?</a>
            </div>
            <button
              type="submit"
              className="w-full bg-academic-blue text-white rounded-lg py-3 font-semibold hover:brightness-110 transition disabled:opacity-50"
              disabled={loading}
            >
              {loading ? "Signing in..." : "Sign In"}
            </button>
          </form>

          <div className="mt-6 text-center text-sm text-gray-600">
            Don’t have an account?{" "}
            <Link to="/register" className="text-academic-blue font-medium hover:underline">Create an account</Link>
          </div>
          <div className="mt-4 text-xs text-gray-500">
            Secure authentication • Your data is protected
          </div>
        </div>
      </div>
    </div>
  );
}
