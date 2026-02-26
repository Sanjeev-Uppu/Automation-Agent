import { api } from "../services/api";
import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useNavigate, useLocation } from "react-router-dom";

export default function ChatPage() {

  // ---------------- STATE ----------------
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();
  const location = useLocation();
  const bottomRef = useRef(null);

  const { grade, subject, chapter_name } = location.state || {};

  // ---------------- SAFETY ----------------
  if (!grade || !subject) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-black text-white">
        Please select grade and subject first.
      </div>
    );
  }

  // ---------------- AUTO SCROLL ----------------
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  // ---------------- HANDLE ASK ----------------
  const handleAsk = async () => {

    if (!question.trim()) return;

    const lower = question.toLowerCase();

    const userMessage = {
      role: "user",
      content: question,
    };

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {

      // ================= MOCK TEST =================
      if (
        (lower.includes("mock") || lower.includes("test")) &&
        !lower.includes("paper")
      ) {

        navigate("/mock", {
          state: { grade, subject, chapter_name }
        });

        setQuestion("");
        return;
      }

      // ================= CALL BACKEND =================
      // ================= CALL BACKEND =================
const data = await api.post("/ask/", {
  question,
  grade,
  subject,
  chapter_name,
});

      // ================= QUESTION PAPER INTENT =================
      // ================= QUESTION PAPER =================
if (lower.includes("question paper")) {

  navigate("/question-paper-setup", {
    state: { grade, subject, chapter_name }
  });

  setQuestion("");
  setLoading(false);
  return;
}

      // ================= NORMAL RESPONSE =================
      const botMessage = {
        role: "bot",
        type: data.type || "text",
        message: data.answer || data.message || "No response",
        download_url: data.download_url || null,
      };

      setMessages((prev) => [...prev, botMessage]);
      setQuestion("");

    } catch (error) {

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          type: "text",
          message: "Something went wrong.",
        },
      ]);

    } finally {
      setLoading(false);
    }
  };

  // ================= UI =================
  return (
    <div className="min-h-screen flex items-center justify-center 
    bg-gradient-to-br from-black via-slate-900 to-purple-950 px-6 py-12">

      <div className="w-full max-w-6xl flex flex-col 
      h-[88vh] bg-white/10 backdrop-blur-xl 
      border border-white/20 rounded-3xl 
      shadow-[0_30px_80px_rgba(0,0,0,0.8)] overflow-hidden">

        {/* Header */}
        <div className="px-8 py-5 border-b border-white/10 bg-black/40">
          <h2 className="text-3xl font-bold text-white">
            AI Lesson Assistant
          </h2>
          <p className="text-gray-300 mt-1">
            Grade {grade} • {subject} • {chapter_name || "All Chapters"}
          </p>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-8 space-y-6">
          <AnimatePresence>
            {messages.map((msg, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.2 }}
              >

                {msg.role === "user" && (
                  <div className="flex justify-end">
                    <div className="bg-gradient-to-r from-cyan-500 to-blue-600 
                    px-5 py-3 rounded-2xl text-white max-w-[60%]">
                      {msg.content}
                    </div>
                  </div>
                )}

                {msg.role === "bot" && (
                  <div className="flex justify-start">
                    <div className="bg-black/80 border border-white/10 
                    rounded-2xl p-5 max-w-[70%] text-white">

                      <p className="whitespace-pre-wrap">
                        {msg.message}
                      </p>

                      {msg.type === "pdf" && msg.download_url && (
                        <motion.button
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                          onClick={() =>
                            window.open(msg.download_url, "_blank")
                          }
                          className="mt-4 px-4 py-2 bg-green-600 rounded-lg"
                        >
                          Download PDF
                        </motion.button>
                      )}

                    </div>
                  </div>
                )}

              </motion.div>
            ))}
          </AnimatePresence>

          {loading && (
            <div className="text-cyan-400 animate-pulse">
              🤖 AI is generating...
            </div>
          )}

          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className="p-6 border-t border-white/10 flex gap-4 bg-black/50">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask your question..."
            className="flex-1 bg-black/80 border border-white/20 
            px-5 py-3 rounded-xl text-white focus:outline-none"
            onKeyDown={(e) => {
              if (e.key === "Enter") handleAsk();
            }}
          />

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleAsk}
            className="px-6 py-3 rounded-xl 
            bg-gradient-to-r from-pink-500 via-cyan-500 to-green-400
            text-white font-semibold"
          >
            Ask
          </motion.button>
        </div>

      </div>
    </div>
  );
}