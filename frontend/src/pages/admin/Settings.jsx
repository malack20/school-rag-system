import React, { useEffect, useState } from "react";
import { useThemeContext } from "../../context/ThemeContext.jsx";

export default function Settings() {
  const { theme, setTheme, toggleTheme } = useThemeContext();
  const [name, setName] = useState(() => localStorage.getItem("account_name") || "");
  const [email, setEmail] = useState(() => localStorage.getItem("account_email") || "");
  const [saving, setSaving] = useState(false);
  const [savedMsg, setSavedMsg] = useState("");

  const onSave = async () => {
    setSaving(true);
    setSavedMsg("");
    setTimeout(() => {
      localStorage.setItem("account_name", name);
      localStorage.setItem("account_email", email);
      setSaving(false);
      setSavedMsg("Saved");
      setTimeout(() => setSavedMsg(""), 1500);
    }, 600);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-6 dark:bg-gray-900 dark:text-gray-100">
      <div className="max-w-4xl mx-auto">
        <div className="text-xl font-semibold mb-4">Settings</div>
        <div className="grid gap-4">
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="font-medium">Theme</div>
            <div className="text-sm text-gray-400 mb-3">Switch between light and dark.</div>
            <div className="flex items-center gap-3">
              <button
                className={`px-3 py-2 rounded-md ${theme === "light" ? "bg-white text-gray-900" : "bg-gray-700 text-gray-200"}`}
                onClick={() => setTheme("light")}
              >
                Light
              </button>
              <button
                className={`px-3 py-2 rounded-md ${theme === "dark" ? "bg-white text-gray-900" : "bg-gray-700 text-gray-200"}`}
                onClick={() => setTheme("dark")}
              >
                Dark
              </button>
              <button
                className="px-3 py-2 rounded-md bg-gray-700 text-gray-200"
                onClick={toggleTheme}
              >
                Toggle
              </button>
              <div className="text-xs text-gray-300 ml-2">Current: {theme}</div>
            </div>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="font-medium">Account</div>
            <div className="text-sm text-gray-400 mb-3">Edit your display name and email.</div>
            <div className="grid gap-3">
              <div>
                <label className="block text-sm text-gray-300 mb-1">Full Name</label>
                <input
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full px-3 py-2 rounded-md bg-gray-700 text-white outline-none focus:ring-2 focus:ring-academic-cyan"
                  placeholder="Jane Student"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-300 mb-1">Email Address</label>
                <input
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  type="email"
                  className="w-full px-3 py-2 rounded-md bg-gray-700 text-white outline-none focus:ring-2 focus:ring-academic-cyan"
                  placeholder="example@student.school.edu"
                />
              </div>
              <div className="flex items-center gap-3">
                <button
                  onClick={onSave}
                  disabled={saving}
                  className="px-4 py-2 rounded-md bg-academic-cyan text-gray-900 font-semibold disabled:opacity-60"
                >
                  {saving ? "Saving..." : "Save"}
                </button>
                {savedMsg && <div className="text-sm text-green-400">{savedMsg}</div>}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
