import React from "react";

export default function MessageBubble({ role, text }) {
  const isUser = role === "user";
  const bg = isUser ? "#e1f5fe" : "#fff";
  return <div style={{ background: bg, padding: 10, margin: 8, borderRadius: 8 }}>{text}</div>;
}
