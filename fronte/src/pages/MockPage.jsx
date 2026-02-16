import { useLocation } from "react-router-dom";
import { useState, useEffect } from "react";

export default function MockPage() {
  const location = useLocation();
  const mockData = location.state;

  const [answers, setAnswers] = useState({});
  const [timeLeft, setTimeLeft] = useState(
    mockData?.duration_minutes * 60 || 0
  );
  const [started, setStarted] = useState(false);
  const [result, setResult] = useState(null);

  // TIMER
  useEffect(() => {
    if (started && timeLeft > 0) {
      const timer = setInterval(() => {
        setTimeLeft((prev) => prev - 1);
      }, 1000);
      return () => clearInterval(timer);
    }

    if (timeLeft === 0 && started) {
      handleSubmit();
    }
  }, [started, timeLeft]);

  const handleSelect = (id, option) => {
    setAnswers((prev) => ({
      ...prev,
      [id]: option,
    }));
  };

  const handleSubmit = async () => {
    const submission = {
      questions: mockData.questions.map((q) => ({
        question_id: q.id,
        selected_answer: answers[q.id] || "",
        correct_answer: q.correct_answer,
      })),
    };

    const response = await fetch(
      "http://127.0.0.1:8002/submit-mock/",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(submission),
      }
    );

    const data = await response.json();
    setResult(data);
  };

  const downloadQuestionPaper = async () => {
    const response = await fetch(
      "http://127.0.0.1:8002/download-exam-pdf/",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          grade: 5,
          subject: "science",
          chapter_name: mockData.chapter,
        }),
      }
    );

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "Question_Paper.pdf";
    a.click();
  };

  if (!mockData) {
    return (
      <div className="text-white text-center mt-10">
        No Mock Test Available
      </div>
    );
  }

  const totalMarks = mockData.questions.length * 2;

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-indigo-950 to-purple-950 text-white p-10">

      {/* EXAM HEADER */}
      <div className="bg-white/5 backdrop-blur-xl p-6 rounded-3xl border border-white/10 mb-8">
        <h1 className="text-3xl font-bold text-cyan-400">
          Olympiad Mock Examination
        </h1>

        <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-300">
          <div><b>Chapter:</b> {mockData.chapter}</div>
          <div><b>Questions:</b> {mockData.questions.length}</div>
          <div><b>Total Marks:</b> {totalMarks}</div>
          <div><b>Duration:</b> {mockData.duration_minutes} mins</div>
        </div>
      </div>

      {!started && (
        <div className="flex gap-4">
          <button
            onClick={() => setStarted(true)}
            className="px-6 py-3 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-xl font-semibold"
          >
            Start Exam
          </button>

          <button
            onClick={downloadQuestionPaper}
            className="px-6 py-3 bg-purple-700 rounded-xl"
          >
            Download Question Paper PDF
          </button>
        </div>
      )}

      {started && !result && (
        <>
          <div className="text-lg text-yellow-400 mb-6">
            Time Left: {Math.floor(timeLeft / 60)}:
            {String(timeLeft % 60).padStart(2, "0")}
          </div>

          {mockData.questions.map((q, index) => (
            <div
              key={q.id}
              className="bg-black/60 p-6 rounded-xl border border-white/10 space-y-3 mb-6"
            >
              <p className="font-semibold">
                Q{index + 1}. {q.question}
                <span className="text-sm text-gray-400 ml-2">(2 Marks)</span>
              </p>

              {q.options.map((option) => (
                <label key={option} className="block cursor-pointer">
                  <input
                    type="radio"
                    name={`q${q.id}`}
                    value={option}
                    onChange={() => handleSelect(q.id, option)}
                    className="mr-2"
                  />
                  {option}
                </label>
              ))}
            </div>
          ))}

          <button
            onClick={handleSubmit}
            className="px-6 py-3 bg-green-600 rounded-xl"
          >
            Submit Exam
          </button>
        </>
      )}

      {result && (
        <div className="bg-black/70 p-6 rounded-xl border border-white/10 mt-8">
          <h3 className="text-xl font-bold text-green-400 mb-4">
            Examination Result
          </h3>
          <p>Total Questions: {result.total_questions}</p>
          <p>Correct Answers: {result.correct}</p>
          <p>Score: {result.percentage}%</p>
        </div>
      )}
    </div>
  );
}
