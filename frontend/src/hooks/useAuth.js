import { useState } from "react";
import { login } from "../services/authService.js";

export default function useAuth() {
  const [user, setUser] = useState(null);
  const signin = async (username, password) => {
    const res = await login(username, password);
    setUser(res.user);
  };
  return { user, signin };
}
