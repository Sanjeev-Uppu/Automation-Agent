import { useState } from "react";
import { askQuestion } from "../services/api";
import StructuredResponse from "../components/chat/StructuredResponse";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

export default function ChatPage() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleAsk = async () => {
    if (!question.trim()) return;

    const userMessage = {
      role: "user",
      content: question,
    };

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const lower = question.toLowerCase();

      // 🔥 MOCK FLOW
      if (lower.includes("mock") || lower.includes("test")) {
        const response = await fetch(
          "http://127.0.0.1:8002/generate-mock/",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              grade: 5,
              subject: "science",
              chapter_name: "Animals",
            }),
          }
        );

        if (!response.ok) {
          throw new Error("Failed to generate mock test");
        }

        const mockData = await response.json();

        navigate("/mock", { state: mockData });
        setQuestion("");
        return;
      }

      // 🔥 NORMAL QA FLOW
      const data = await askQuestion({
        question,
        grade: 5,
        subject: "science",
        chapter_name: "Animals",
      });

      const botMessage = {
        role: "bot",
        structured: data,
      };

      setMessages((prev) => [...prev, botMessage]);
      setQuestion("");

    } catch (error) {
      console.error("Error:", error);

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          structured: {
            answer_type: "explanation",
            explanation: "Something went wrong. Please try again.",
          },
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[80vh] bg-white/5 backdrop-blur-2xl border border-white/10 rounded-3xl shadow-2xl overflow-hidden">

      {/* Header */}
      <div className="px-6 py-4 border-b border-white/10 bg-gradient-to-r from-cyan-500/10 to-purple-500/10">
        <h2 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
          AI Lesson Assistant
        </h2>
        <p className="text-sm text-gray-400 mt-1">
          Ask questions or generate a mock test.
        </p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((msg, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            {msg.role === "user" && (
              <div className="flex justify-end">
                <div className="bg-gradient-to-r from-cyan-500 to-blue-600 px-5 py-3 rounded-2xl text-white shadow-lg max-w-lg">
                  {msg.content}
                </div>
              </div>
            )}

            {msg.role === "bot" && (
              <div className="flex justify-start">
                <div className="bg-black/70 border border-white/10 rounded-2xl p-6 shadow-xl max-w-3xl w-full">
                  <StructuredResponse response={msg.structured} />
                </div>
              </div>
            )}
          </motion.div>
        ))}

        {loading && (
          <div className="text-cyan-400 animate-pulse">
            🤖 AI is thinking...
          </div>
        )}
      </div>

      {/* Input Section */}
      <div className="p-4 border-t border-white/10 flex gap-4 bg-black/40">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question or type 'Generate mock test'..."
          className="flex-1 bg-black/60 border border-white/10 px-5 py-3 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-cyan-400"
          onKeyDown={(e) => {
            if (e.key === "Enter") handleAsk();
          }}
        />

        <button
          onClick={handleAsk}
          className="px-6 py-3 rounded-xl bg-gradient-to-r from-cyan-500 to-purple-600 hover:scale-105 active:scale-95 transition-all shadow-lg"
        >
          Ask
        </button>
      </div>
    </div>
  );
}
