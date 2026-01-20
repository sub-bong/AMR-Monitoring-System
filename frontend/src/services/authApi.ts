import { API_BASE } from "./api";

type TokenResponse = { access_token: string; token_type: string };

async function postJson<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) throw new Error(await res.text());

  return res.json();
}

export async function login(email: string, password: string) {
  const res = await postJson<TokenResponse>("/auth/login", { email, password });
  return res.access_token;
}

export async function register(email: string, password: string) {
  const res = await postJson<TokenResponse>("/auth/register", { email, password });
  return res.access_token;
}

export async function deviceAuth(device_key: string) {
  const res = await postJson<TokenResponse>("/auth/device", { device_key });
  return res.access_token;
}
