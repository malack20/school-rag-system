import api from "./api";

export async function sendMessage(content) {
  const { data } = await api.post("/api/chat/", { content });
  return data;
}

export async function answerMessage(content) {
  const { data } = await api.post("/api/chat/answer", { content });
  return data;
}
