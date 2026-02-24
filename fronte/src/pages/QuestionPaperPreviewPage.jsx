import { useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";

export default function QuestionPaperPreviewPage() {

  const location = useLocation();
  const navigate = useNavigate();

  const initialPaper = location.state?.paper_data;
  const [paperData, setPaperData] = useState(initialPaper);
  const [showModifyBox, setShowModifyBox] = useState(false);
  const [modificationText, setModificationText] = useState("");
  const [loading, setLoading] = useState(false);

  if (!paperData) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-black text-white">
        No preview available.
      </div>
    );
  }

  const handleModify = async () => {
    if (!modificationText.trim()) return;

    setLoading(true);

    const response = await fetch(
      "http://127.0.0.1:8002/modify-question-paper/",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          original_paper: paperData,
          modification_request: modificationText
        })
      }
    );

    const data = await response.json();

    if (data.paper_data) {
      setPaperData(data.paper_data);
      setShowModifyBox(false);
      setModificationText("");
    }

    setLoading(false);
  };

  const handleDownload = async () => {

    const response = await fetch(
      "http://127.0.0.1:8002/generate-question-paper-pdf/",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          paper_data: paperData
        })
      }
    );

    const data = await response.json();

    if (data.download_url) {
      window.open(data.download_url, "_blank");
    }
  };

  return (
    <div className="min-h-screen bg-black text-white p-8">

      <h2 className="text-3xl font-bold mb-4">
        {paperData.school_name}
      </h2>

      <p className="mb-6">
        Grade {paperData.grade} • {paperData.subject} • {paperData.chapter}
      </p>

      {/* Questions */}
      <div className="space-y-6 bg-gray-900 p-6 rounded-xl">
        {paperData.questions.map((q, index) => (
          <div key={index}>
            <p className="font-semibold">
              Q{index + 1}. {q.question}
            </p>
            <ul className="ml-4 mt-2 list-disc">
              {q.options.map((opt, i) => (
                <li key={i}>{opt}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      {/* Buttons */}
      <div className="mt-6 flex gap-4">
        <button
          onClick={handleDownload}
          className="bg-green-600 px-4 py-2 rounded"
        >
          Download PDF
        </button>

        <button
          onClick={() => setShowModifyBox(true)}
          className="bg-yellow-600 px-4 py-2 rounded"
        >
          Modify
        </button>

        <button
          onClick={() => navigate("/chat")}
          className="bg-cyan-600 px-4 py-2 rounded"
        >
          Back to Chat
        </button>
      </div>

      {/* Modify Box */}
      {showModifyBox && (
        <div className="mt-6 bg-gray-800 p-4 rounded-xl">
          <textarea
            placeholder="Enter your modifications here..."
            value={modificationText}
            onChange={(e) => setModificationText(e.target.value)}
            className="w-full p-2 bg-black border border-gray-600 rounded"
          />

          <button
            onClick={handleModify}
            className="mt-2 bg-pink-600 px-4 py-2 rounded"
          >
            {loading ? "Regenerating..." : "Regenerate"}
          </button>
        </div>
      )}
    </div>
  );
}