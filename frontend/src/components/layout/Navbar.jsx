import React from "react";

export default function Navbar({ onNavigate }) {
  return (
    <div style={{ background: "#282c34", color: "#fff", padding: 12, display: "flex", gap: 12 }}>
      <div style={{ fontWeight: "bold" }}>School RAG</div>
      <button onClick={() => onNavigate("chat")}>Chat</button>
    </div>
  );
}
