import { useState } from "react";
import { deviceAuth, login, register } from "../services/authApi";
import { useAuth } from "../hooks/auth/useAuth";

export default function AuthPage() {
  const { userToken, deviceToken, setUserToken, setDeviceToken, clearTokens } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [deviceKey, setDeviceKey] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState<"login" | "register" | "device" | "">("");

  const tokenLabel = (t: string) => (t ? `${t.slice(0, 12)}...` : "없음");

  async function handleLogin() {
    try {
      setBusy("login");
      setError("");
      const token = await login(email, password);
      setUserToken(token);
    } catch (e) {
      setError(e instanceof Error ? e.message : "로그인 실패");
    } finally {
      setBusy("");
    }
  }

  async function handleRegister() {
    try {
      setBusy("register");
      setError("");
      const token = await register(email, password);
      setUserToken(token);
    } catch (e) {
      setError(e instanceof Error ? e.message : "회원가입 실패");
    } finally {
      setBusy("");
    }
  }

  async function handleDeviceAuth() {
    try {
      setBusy("device");
      setError("");
      const token = await deviceAuth(deviceKey);
      setDeviceToken(token);
    } catch (e) {
      setError(e instanceof Error ? e.message : "디바이스 인증 실패");
    } finally {
      setBusy("");
    }
  }

  return (
    <div className="mx-auto max-w-4xl px-6 py-10">
      <h1 className="mb-6 text-2xl font-semibold">인증</h1>

      {error && <div className="mb-4 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>}

      <div className="grid gap-6 md:grid-cols-2">
        <div className="rounded-2xl border border-slate-200 bg-white/70 p-5 shadow-sm">
          <h2 className="mb-3 text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">사용자</h2>
          <div className="space-y-3">
            <input className="w-full text-slate-600 rounded-lg border px-3 py-2" placeholder="이메일" value={email} onChange={(e) => setEmail(e.target.value)} />
            <input
              className="w-full text-slate-600 rounded-lg border px-3 py-2"
              type="password"
              placeholder="비밀번호"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <div className="flex gap-2">
              <button className="cursor-pointer rounded-lg bg-slate-900 px-4 py-2 text-sm text-white disabled:opacity-50" onClick={handleLogin} disabled={busy === "login"}>
                로그인
              </button>
              <button
                className="cursor-pointer rounded-lg text-slate-600 border border-slate-300 px-4 py-2 text-sm disabled:opacity-50"
                onClick={handleRegister}
                disabled={busy === "register"}
              >
                회원가입
              </button>
            </div>
            <div className="text-xs text-slate-500">User 토큰: {tokenLabel(userToken)}</div>
          </div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white/70 p-5 shadow-sm">
          <h2 className="mb-3 text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">디바이스</h2>
          <div className="space-y-3">
            <input className="w-full text-slate-600 rounded-lg border px-3 py-2" placeholder="Device Key" value={deviceKey} onChange={(e) => setDeviceKey(e.target.value)} />
            <button className="cursor-pointer rounded-lg bg-blue-600 px-4 py-2 text-sm text-white disabled:opacity-50" onClick={handleDeviceAuth} disabled={busy === "device"}>
              디바이스 토큰 발급
            </button>
            <div className="text-xs text-slate-500">Device 토큰: {tokenLabel(deviceToken)}</div>
          </div>
        </div>
      </div>

      <button className="mt-6 text-sm text-slate-500 underline" onClick={clearTokens}>
        토큰 초기화
      </button>
    </div>
  );
}
