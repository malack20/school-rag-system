import React from "react";
import MessageBubble from "./MessageBubble.jsx";

export default function ChatBox({ messages }) {
  return (
    <div>
      {messages.map((m, i) => (
        <MessageBubble key={i} role={m.role} text={m.text} />
      ))}
    </div>
  );
}
