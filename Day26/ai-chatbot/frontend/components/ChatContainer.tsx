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

  const API_URL = process.env.NEXT_PUBLIC_API_URL;

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

  const clearChat = () => {
    setMessages([]);
  };

  useEffect(() => {
    const messagesContainer = document.getElementById("messages-container");
    if (messagesContainer) {
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="w-full h-[90vh] max-w-2xl flex flex-col bg-white rounded-2xl shadow-xl overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 px-6 py-4 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-white">AI Support Chat</h1>
          <p className="text-blue-100 text-sm mt-1">
            Powered by FastAPI + Next.js
          </p>
        </div>
        {messages.length > 0 && (
          <button
            onClick={clearChat}
            className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200"
          >
            Clear
          </button>
        )}
      </div>

      {/* Messages Container */}
      <div
        id="messages-container"
        className="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-50"
      >
        {messages.length === 0 && (
          <div className="flex items-center justify-center h-full text-gray-400">
            <div className="text-center">
              <div className="text-4xl mb-2">👋</div>
              <p className="text-lg">Start a conversation below!</p>
            </div>
          </div>
        )}

        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`px-4 py-2 rounded-2xl max-w-xs lg:max-w-md text-sm leading-relaxed ${
                msg.role === "user"
                  ? "bg-blue-600 text-white rounded-br-none"
                  : "bg-white text-gray-800 rounded-bl-none border border-gray-200 shadow-sm"
              }`}
            >
              {msg.message}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="px-4 py-3 bg-white text-gray-600 rounded-2xl rounded-bl-none text-sm border border-gray-200 shadow-sm">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 px-6 py-4">
        <div className="flex gap-3">
          <input
            type="text"
            placeholder="Type your message..."
            className="flex-1 border border-gray-300 rounded-full px-5 py-3 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent transition-all duration-200 text-sm text-black"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={loading}
          />
          <button
            onClick={() => sendMessage(input)}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-full font-medium transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-md hover:shadow-lg"
          >
            {loading ? "..." : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
}