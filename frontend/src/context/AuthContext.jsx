import React, { createContext, useState, useContext } from "react";
import { login } from "../services/authService.js";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const signin = async (username, password) => {
    const res = await login(username, password);
    setUser(res.user);
  };
  const value = { user, signin };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuthContext() {
  return useContext(AuthContext);
}
