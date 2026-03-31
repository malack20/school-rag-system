import React from "react";

export default function TypingIndicator({ visible }) {
  if (!visible) return null;
  return (
    <div className="flex items-center gap-2 mt-2">
      <div className="rounded-2xl px-3 py-2 bg-gray-800 text-white inline-flex items-center gap-1">
        <span className="typing-dot" style={{ animationDelay: "0s" }} />
        <span className="typing-dot" style={{ animationDelay: "0.15s" }} />
        <span className="typing-dot" style={{ animationDelay: "0.3s" }} />
      </div>
      <span className="text-gray-400 text-xs">Thinking...</span>
    </div>
  );
}
