import { useCallback, useMemo, useState } from "react";
import { AuthContext } from "../hooks/auth/authContext";

function readToken(key: string) {
  return localStorage.getItem(key) ?? "";
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [userToken, setUserTokenState] = useState(() => readToken("userToken"));
  const [deviceToken, setDeviceTokenState] = useState(() => readToken("deviceToken"));

  const setUserToken = (token: string) => {
    setUserTokenState(token);
    if (token) localStorage.setItem("userToken", token);
    else localStorage.removeItem("userToken");
  };

  const setDeviceToken = (token: string) => {
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
