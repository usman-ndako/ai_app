"use client";

import { useState } from "react";

export default function ChatInput({ onSend }: { onSend: (msg: string) => void }) {
  const [input, setInput] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    onSend(input);
    setInput("");
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex items-center gap-2 p-3 bg-white border-t"
    >
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type a message..."
        className="flex-1 border rounded-full px-4 py-2 outline-none focus:ring-2 focus:ring-blue-400"
      />
      <button
        type="submit"
        className="bg-blue-600 text-white px-4 py-2 rounded-full hover:bg-blue-700 transition"
      >
        Send
      </button>
    </form>
  );
}
