import { useState } from "react";
import { sendMessage } from "../services/chatService.js";

export default function useChat() {
  const [messages, setMessages] = useState([]);
  const send = async (text) => {
    setMessages((m) => [...m, { role: "user", text }]);
    const res = await sendMessage(text);
    setMessages((m) => [...m, { role: "assistant", text: res.response || "" }]);
  };
  return { messages, send };
}
