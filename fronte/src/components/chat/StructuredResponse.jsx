export default function StructuredResponse({ response }) {

  if (!response) return null;

  // LIST RESPONSE
  if (response.answer_type === "list" && Array.isArray(response.data)) {
    return (
      <div>
        <div className="mb-3 text-sm text-cyan-400">
          {response.count || response.data.length} Results Found
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {response.data.map((item, index) => (
            <div
              key={index}
              className="bg-gradient-to-br from-cyan-500/10 to-purple-500/10 
                         border border-white/10 p-3 rounded-xl 
                         hover:scale-105 transition"
            >
              {typeof item === "string" ? item.replace(/\.$/, "") : item}
            </div>
          ))}
        </div>
      </div>
    );
  }

  // TEXT RESPONSE
  return (
    <div className="text-gray-300 whitespace-pre-wrap">
      {response.answer || response.explanation || "No answer available"}
    </div>
  );
}
