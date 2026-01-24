import { useCallback, useMemo, useState } from "react";
import { AuthContext } from "../hooks/auth/authContext";

function getJwtExp(token: string): number | null {
  try {
    const payload = token.split(".")[1];
    if (!payload) return null;
    const json = JSON.parse(atob(payload.replace(/-/g, "+").replace(/_/g, "/")));
    return typeof json.exp === "number" ? json.exp : null;
  } catch {
    return null;
  }
}

function isTokenExpired(token: string): boolean {
  const exp = getJwtExp(token);
  if (!exp) return true; // 해석 불가하면 만료 처리
  return Date.now() / 1000 >= exp;
}

function readToken(key: string) {
  const token = localStorage.getItem(key) ?? "";

  if (!token) return "";
  if (isTokenExpired(token)) {
    localStorage.removeItem(key);
    return "";
  }
  return token;
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [userToken, setUserTokenState] = useState(() => readToken("userToken"));
  const [deviceToken, setDeviceTokenState] = useState(() => readToken("deviceToken"));

  const setUserToken = (token: string) => {
    if (token && isTokenExpired(token)) {
      localStorage.removeItem("userToken");
      setUserTokenState("");
      return;
    }
    setUserTokenState(token);
    if (token) localStorage.setItem("userToken", token);
    else localStorage.removeItem("userToken");
  };

  const setDeviceToken = (token: string) => {
    if (token && isTokenExpired(token)) {
      localStorage.removeItem("deviceToken");
      setDeviceTokenState("");
      return;
    }
    setDeviceTokenState(token);
    if (token) localStorage.setItem("deviceToken", token);
    else localStorage.removeItem("deviceToken");
  };

  const clearTokens = useCallback(() => {
    setUserToken("");
    setDeviceToken("");
  }, []);

  const value = useMemo(() => ({ userToken, deviceToken, setUserToken, setDeviceToken, clearTokens }), [userToken, deviceToken, clearTokens]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
