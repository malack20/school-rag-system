import api from "./api";

export async function register(username, email, password) {
  const { data } = await api.post("/api/auth/register/", { username, email, password });
  return data;
}

export async function login(emailOrUsername, password) {
  const payload = { username: emailOrUsername, password };
  const { data } = await api.post("/api/auth/login/", payload);
  return data;
}
