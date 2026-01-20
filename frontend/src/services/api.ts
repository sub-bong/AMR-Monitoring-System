export const API_BASE = import.meta.env.VITE_API_BASE as string;

if (!API_BASE) throw new Error("ENV API 값이 비었습니다.");

export async function apiGet<T>(path: string, token?: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: token ? { Authorization: `Bearer ${token}` } : undefined,
  });

  if (!res.ok) throw new Error(await res.text());

  return res.json();
}
