import React from "react";

export default function Modal({ open, children }) {
  if (!open) return null;
  return <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,.3)" }}>{children}</div>;
}
