"use client";

interface ChatBubbleProps {
  role: "user" | "bot";
  message: string;
}

export default function ChatBubble({ role, message }: ChatBubbleProps) {
  const isUser = role === "user";
  return (
    <div
      className={`flex ${isUser ? "justify-end" : "justify-start"} my-2`}
    >
      <div
        className={`max-w-[70%] p-3 rounded-2xl shadow-md ${
          isUser
            ? "bg-blue-600 text-white rounded-br-none"
            : "bg-white text-gray-900 rounded-bl-none"
        }`}
      >
        {message}
      </div>
    </div>
  );
}
