import React, { useState } from "react";

export default function ChatInput({ onSend }) {
  const [text, setText] = useState("");
  const send = () => {
    if (!text.trim()) return;
    onSend(text);
    setText("");
  };
  return (
    <div style={{ display: "flex", gap: 8 }}>
      <input value={text} onChange={(e) => setText(e.target.value)} style={{ flex: 1 }} />
      <button onClick={send}>Send</button>
    </div>
  );
}
