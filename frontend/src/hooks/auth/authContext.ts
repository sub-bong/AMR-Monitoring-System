import { createContext } from "react";

export type AuthContextValue = {
  userToken: string;
  deviceToken: string;
  setUserToken: (token: string) => void;
  setDeviceToken: (token: string) => void;
  clearTokens: () => void;
};

export const AuthContext = createContext<AuthContextValue | undefined>(undefined);
