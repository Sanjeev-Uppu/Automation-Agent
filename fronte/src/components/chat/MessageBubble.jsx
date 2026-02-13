export default function MessageBubble({ message, isUser }) {
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}>
      <div
        className={`px-5 py-3 max-w-xl rounded-2xl shadow-lg ${
          isUser
            ? "bg-gradient-to-r from-cyan-500 to-blue-600 text-white"
            : "bg-white/10 backdrop-blur-lg border border-white/20 text-gray-200"
        }`}
      >
        {message}
      </div>
    </div>
  );
}
