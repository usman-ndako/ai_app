"use client";

import { useEffect, useState } from "react";
import { v4 as uuidv4 } from "uuid";

interface Message {
  id: string;
  role: "user" | "bot";
  message: string;
}

export default function ChatContainer() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string>("");

  // ---------- PERSISTENT MEMORY WITH LOCALSTORAGE ----------
  const STORAGE_KEY = "chat_messages";
  const loadMessages = (): Message[] => {
    if (typeof window === "undefined") return [];
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  };

  const saveMessages = (msgs: Message[]) => {
    if (typeof window === "undefined") return;
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(msgs));
    } catch {
      // Ignore errors
    }
  };

  // Load on mount
  useEffect(() => {
    const loaded = loadMessages();
    setMessages(loaded);
  }, []);

  // Save on messages change
  useEffect(() => {
    saveMessages(messages);
  }, [messages]);

  // Generate or load session_id once
  useEffect(() => {
    const existing = localStorage.getItem("chat_session_id");
    if (existing) {
      setSessionId(existing);
    } else {
      const newId = uuidv4();
      localStorage.setItem("chat_session_id", newId);
      setSessionId(newId);
    }
  }, []);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

  const sendMessage = async (text: string) => {
    if (!text.trim() || !sessionId) return;

    const userId = uuidv4();
    const userMessage: Message = { id: userId, role: "user", message: text };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: sessionId,
          message: text,
        }),
      });

      if (!res.ok) {
        console.error("Backend error:", res.statusText);
        const botId = uuidv4();
        setMessages((prev) => [
          ...prev,
          { id: botId, role: "bot", message: "Server error. Please try again." },
        ]);
        return;
      }

      const data = await res.json();
      console.log("Backend response:", data);

      const botId = uuidv4();
      setMessages((prev) => [
        ...prev,
        { id: botId, role: "bot", message: data.reply || "No response received." },
      ]);
    } catch (error) {
      console.error("Error sending message:", error);
      const botId = uuidv4();
      setMessages((prev) => [
        ...prev,
        { id: botId, role: "bot", message: "Failed to connect to backend." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !loading) {
      sendMessage(input);
    }
  };

  // Optional: Clear chat button
  const clearChat = () => {
    setMessages([]);
    localStorage.removeItem(STORAGE_KEY);
  };

  return (
    <div className="flex flex-col items-center justify-between w-full max-w-3xl h-[90vh] mx-auto p-6 bg-white border rounded-2xl shadow-lg">
      <div className="w-full text-center mb-4 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">AI Support Chat</h1>
          <p className="text-sm text-gray-500">
            Powered by FastAPI + Next.js + Memory (Persistent)
          </p>
        </div>
        {messages.length > 0 && (
          <button
            onClick={clearChat}
            className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 text-sm"
          >
            Clear
          </button>
        )}
      </div>

      <div className="flex-1 w-full overflow-y-auto border rounded-lg p-4 bg-gray-50 mb-4 space-y-3">
        {messages.length === 0 && (
          <p className="text-gray-400 text-center">
            👋 Start a conversation below!
          </p>
        )}

        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`px-4 py-2 rounded-2xl text-sm max-w-[75%] ${
                msg.role === "user"
                  ? "bg-blue-500 text-white"
                  : "bg-gray-200 text-gray-800"
              }`}
            >
              {msg.message}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="px-4 py-2 bg-gray-200 text-gray-600 rounded-2xl text-sm animate-pulse">
              Typing...
            </div>
          </div>
        )}
      </div>

      <div className="flex w-full items-center space-x-3">
        <input
          type="text"
          placeholder="Type your message..."
          className="flex-1 border border-gray-300 rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
        />
        <button
          onClick={() => sendMessage(input)}
          disabled={loading}
          className="bg-blue-500 text-white px-5 py-2 rounded-full hover:bg-blue-600 transition disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  );
}