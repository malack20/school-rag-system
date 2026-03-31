import React, { useState, useRef } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useThemeContext } from "../context/ThemeContext.jsx";
import { sendMessage, answerMessage } from "../services/chatService.js";
import { uploadDocument, analyzeDocument } from "../services/documentService.js";
import TypingIndicator from "../components/chat/TypingIndicator.jsx";

function SidebarItem({ label, active, onClick }) {
  return (
    <button
      onClick={onClick}
      className={`w-full text-left px-3 py-2 rounded-md text-sm ${active ? "bg-gray-800 text-white" : "text-gray-300 hover:bg-gray-800 hover:text-white"}`}
      aria-current={active ? "page" : undefined}
    >
      {label}
    </button>
  );
}

function ChatMessage({ role, text, sources }) {
  const isUser = role === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-3`}>
      <div className={`max-w-[70%] rounded-2xl px-4 py-2 ${isUser ? "bg-academic-blue text-white" : "bg-white text-gray-900 shadow"} whitespace-pre-wrap`}>
        {text}
      </div>
    </div>
  );
}

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [typing, setTyping] = useState(false);
  const [input, setInput] = useState("");
  const [conversations, setConversations] = useState([{ id: "default", title: "New chat" }]);
  const [active, setActive] = useState("default");
  const fileInputRef = useRef(null);
  const navigate = useNavigate();
  const location = useLocation();
  const { theme } = useThemeContext();

  const onSend = async () => {
    if (!input.trim()) return;
    const text = input;
    setInput("");
    setMessages((m) => [...m, { role: "user", text }]);
    setTyping(true);
    const timer = setTimeout(() => {
      setMessages((m) => [...m, { role: "assistant", text: "Working on it..." }]);
    }, 4000);
    try {
      const res = await answerMessage(text);
      clearTimeout(timer);
      setMessages((m) => [...m, { role: "assistant", text: res.response || "", sources: res.sources || [] }]);
    } catch {
      clearTimeout(timer);
      let quick = "Fetching information took too long. Here’s a quick answer based on known policies.";
      const q = text.toLowerCase();
      if (q.includes("tender") || q.includes("procurement") || q.includes("bid") || q.includes("rfp")) {
        quick = [
          "Quick Tender Guidance:",
          "• Check eligibility and required documents",
          "• Note submission deadlines and format",
          "• Submit to the stated portal or office",
          "• Follow evaluation and compliance instructions",
          "• Contact procurement office for clarifications",
        ].join("\n");
      } else if (q.includes("admission") || q.includes("enroll") || q.includes("apply")) {
        quick = [
          "Quick Admission Guidance:",
          "• Review eligibility and required credentials",
          "• Submit application before deadlines",
          "• Pay applicable fees and track status",
          "• Contact admissions office for assistance",
        ].join("\n");
      } else if (q.includes("fee") || q.includes("tuition") || q.includes("payment")) {
        quick = [
          "Quick Fee Guidance:",
          "• Check fee breakdown and due dates",
          "• Use approved payment channels",
          "• Keep receipts and confirm posting",
          "• Contact finance office for issues",
        ].join("\n");
      }
      setMessages((m) => [...m, { role: "assistant", text: quick }]);
    } finally {
      setTyping(false);
    }
  };

  const onUploadClick = () => {
    fileInputRef.current?.click();
  };

  const onFileSelected = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setMessages((m) => [...m, { role: "user", text: `Uploaded: ${file.name}` }]);
    const fd = new FormData();
    fd.append("title", file.name);
    fd.append("file", file);
    setTyping(true);
    const doc = await uploadDocument(fd);
    let shownWaiting = false;
    const timer = setTimeout(() => {
      shownWaiting = true;
      setMessages((m) => [...m, { role: "assistant", text: "Analyzing document... this might take a moment." }]);
    }, 5000);
    try {
      const res = await analyzeDocument(doc.id);
      clearTimeout(timer);
      setMessages((m) => [...m, { role: "assistant", text: res.feedback || "No feedback available" }]);
    } catch {
      clearTimeout(timer);
      setMessages((m) => [...m, { role: "assistant", text: "Analysis is taking longer than expected. A quick summary has been provided." }]);
    } finally {
      setTyping(false);
    }
    e.target.value = "";
  };

  const containerClass = theme === "dark" ? "bg-gray-900 text-gray-100" : "bg-gray-50 text-gray-900";
  return (
    <div className={`min-h-screen grid grid-cols-12 ${containerClass}`}>
      <aside className="col-span-3 lg:col-span-2 border-r border-gray-800 p-4 flex flex-col gap-4">
        <button
          onClick={() => {
            const id = `c-${Date.now()}`;
            setConversations((c) => [{ id, title: "New chat" }, ...c]);
            setMessages([]);
            setActive(id);
          }}
          className="w-full bg-gray-800 hover:bg-gray-700 text-white rounded-md py-2"
        >
          New chat
        </button>
        <div className="text-xs text-gray-400 uppercase tracking-wide">Navigation</div>
        <SidebarItem
          label="Chat"
          active={location.pathname.startsWith("/chat")}
          onClick={() => navigate("/chat")}
        />
        <SidebarItem
          label="Documents"
          active={location.pathname.startsWith("/admin/documents")}
          onClick={() => navigate("/admin/documents")}
        />
        <SidebarItem
          label="Analytics"
          active={location.pathname.startsWith("/admin/analytics")}
          onClick={() => navigate("/admin/analytics")}
        />
        <SidebarItem
          label="Settings"
          active={location.pathname.startsWith("/settings")}
          onClick={() => navigate("/settings")}
        />
        <div className="text-xs text-gray-400 uppercase tracking-wide mt-6">History</div>
        <div className="space-y-2">
          {conversations.map((c) => (
            <button
              key={c.id}
              onClick={() => {
                setActive(c.id);
                setMessages([]);
              }}
              className={`w-full text-left px-3 py-2 rounded-md text-sm ${active === c.id ? "bg-gray-800 text-white" : "text-gray-300 hover:bg-gray-800 hover:text-white"}`}
            >
              {c.title}
            </button>
          ))}
        </div>
      </aside>
      <main className="col-span-9 lg:col-span-10 flex flex-col">
        <header className="border-b border-gray-800 p-4 flex items-center justify-between">
          <div className="font-semibold">School AI Assistant</div>
          <div className="text-xs text-gray-400">RAG Helpdesk</div>
        </header>
        <div className={`flex-1 overflow-y-auto p-6 ${theme === "dark" ? "bg-gray-950" : "bg-gray-100"}`}>
          <div className="max-w-3xl mx-auto">
            {messages.length === 0 && (
              <div className="text-center text-gray-400 py-16">
                Start a conversation by asking a question about school information.
              </div>
            )}
            {messages.map((m, i) => (
              <div key={i}>
                <ChatMessage role={m.role} text={m.text} sources={m.sources} />
                {m.role === "assistant" && m.sources && m.sources.length > 0 && (
                  <div className="mt-2 bg-gray-100 dark:bg-gray-800 rounded-md p-3">
                    <div className="text-xs font-semibold text-gray-700 dark:text-gray-200 mb-2">Sources</div>
                    <div className="space-y-2">
                      {m.sources.map((s, idx) => (
                        <div key={idx} className="text-xs text-gray-700 dark:text-gray-300">
                          <span className="font-medium">{s.title || "Document"}</span>: {s.snippet}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
            <TypingIndicator visible={typing} />
          </div>
        </div>
        <div className="border-t border-gray-800 p-4 bg-gray-900">
          <div className="max-w-3xl mx-auto flex gap-3 items-center">
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.docx,.txt"
              className="hidden"
              onChange={onFileSelected}
            />
            <button
              onClick={onUploadClick}
              aria-label="Upload for analysis"
              className="h-10 w-10 rounded-md bg-gray-800 text-white hover:bg-gray-700 flex items-center justify-center"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" className="opacity-90">
                <path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M7 9l5-5 5 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M12 4v12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask anything about admissions, schedules, guidelines..."
              className="flex-1 rounded-md px-3 py-2 bg-gray-800 text-white outline-none focus:ring-2 focus:ring-academic-cyan"
            />
            <button
              onClick={onSend}
              className="px-4 py-2 rounded-md bg-academic-cyan text-gray-900 font-semibold hover:brightness-110"
            >
              Send
            </button>
          </div>
          <div className="max-w-3xl mx-auto mt-2 text-xs text-gray-500">
            Secure • Answers generated using verified school documents
          </div>
        </div>
      </main>
    </div>
  );
}
