import { useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const chatRef = useRef(null);

  useEffect(() => {
    chatRef.current?.scrollTo({
      top: chatRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    try {
      const response = await fetch("http://127.0.0.1:8002/ask/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: input,
          grade: 5,
          subject: "science",
        }),
      });

      const data = await response.json();

      const botMessage = {
        role: "bot",
        content: data.explanation || data.answer || "No response",
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="relative bg-white/5 backdrop-blur-2xl border border-white/10 rounded-3xl shadow-2xl p-8 flex flex-col h-[75vh]">

      {/* Header */}
      <div className="mb-6">
        <h2 className="text-2xl font-semibold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
          AI Chat Assistant
        </h2>
        <p className="text-sm text-gray-400 mt-1">
          Ask anything from your lesson and get structured answers.
        </p>
      </div>

      {/* Messages */}
      <div
        ref={chatRef}
        className="flex-1 overflow-y-auto space-y-6 pr-2"
      >
        {messages.map((msg, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className={`max-w-2xl px-6 py-4 rounded-2xl text-sm shadow-lg ${
              msg.role === "user"
                ? "ml-auto bg-linear-to-r from-blue-600 to-cyan-500 text-white"
                : "bg-gray-900/80 border border-gray-800 text-gray-200"
            }`}
          >
            {msg.content}
          </motion.div>
        ))}
      </div>

      {/* Input Section */}
      <div className="mt-8 flex items-center gap-4">
        <input
          className="flex-1 bg-gray-900/80 border border-gray-700 rounded-2xl px-6 py-4 text-white focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your question..."
        />

        <button
          onClick={sendMessage}
          className="px-8 py-4 rounded-2xl bg-gradient-to-r from-blue-600 to-cyan-500 hover:scale-105 active:scale-95 transition-all shadow-xl"
        >
          Ask
        </button>
      </div>
    </div>
  );
}
