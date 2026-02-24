import { useLocation } from "react-router-dom";
import { useState, useEffect } from "react";

export default function MockPage() {

  const location = useLocation();
  const { grade, subject, chapter_name } = location.state || {};

  const [questionCount, setQuestionCount] = useState(5);
  const [durationMinutes, setDurationMinutes] = useState(15);

  const [mockData, setMockData] = useState(null);
  const [answers, setAnswers] = useState({});
  const [timeLeft, setTimeLeft] = useState(0);
  const [started, setStarted] = useState(false);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // ---------------- TIMER ----------------
  useEffect(() => {
    if (started && timeLeft > 0) {
      const timer = setInterval(() => {
        setTimeLeft(prev => prev - 1);
      }, 1000);
      return () => clearInterval(timer);
    }

    if (timeLeft === 0 && started) {
      handleSubmit();
    }

  }, [started, timeLeft]);

  // ---------------- GENERATE MOCK ----------------
  const generateMock = async () => {

    setLoading(true);

    const response = await fetch(
      "http://127.0.0.1:8002/generate-mock/",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          grade,
          subject,
          chapter_name,
          number_of_questions: questionCount,
          duration_minutes: durationMinutes,
        }),
      }
    );

    const data = await response.json();

    setMockData(data);
    setTimeLeft(durationMinutes * 60);
    setLoading(false);
  };

  // ---------------- HANDLE ANSWER ----------------
  const handleSelect = (id, option) => {
    setAnswers(prev => ({
      ...prev,
      [id]: option,
    }));
  };

  // ---------------- SUBMIT ----------------
  const handleSubmit = async () => {

    const submission = {
      questions: mockData.questions.map(q => ({
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

  // ---------------- SAFETY ----------------
  if (!grade) {
    return (
      <div className="text-white text-center mt-10">
        Please select grade first.
      </div>
    );
  }

  // ================= UI =================
  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-indigo-950 to-purple-950 text-white p-10">

      <div className="bg-white/5 backdrop-blur-xl p-6 rounded-3xl border border-white/10 mb-8">
        <h1 className="text-3xl font-bold text-cyan-400">
          Mock Exam Setup
        </h1>

        <p className="mt-2 text-gray-300">
          Grade {grade} • {subject} • {chapter_name}
        </p>
      </div>

      {/* ---------- SETUP PANEL ---------- */}
      {!mockData && (
        <div className="bg-black/60 p-6 rounded-xl border border-white/10 space-y-6">

          <div>
            <label>Number of Questions</label>
            <input
              type="number"
              min="1"
              value={questionCount}
              onChange={(e) => setQuestionCount(parseInt(e.target.value))}
              className="block mt-2 px-4 py-2 bg-black border border-white/20 rounded-lg"
            />
          </div>

          <div>
            <label>Duration (minutes)</label>
            <input
              type="number"
              min="1"
              value={durationMinutes}
              onChange={(e) => setDurationMinutes(parseInt(e.target.value))}
              className="block mt-2 px-4 py-2 bg-black border border-white/20 rounded-lg"
            />
          </div>

          <button
            onClick={generateMock}
            className="px-6 py-3 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-xl"
          >
            {loading ? "Generating..." : "Generate Test"}
          </button>
        </div>
      )}

      {/* ---------- START EXAM ---------- */}
      {mockData && !started && (
        <div className="mt-6">
          <button
            onClick={() => setStarted(true)}
            className="px-6 py-3 bg-green-600 rounded-xl"
          >
            Start Exam
          </button>
        </div>
      )}

      {/* ---------- EXAM ---------- */}
      {started && !result && mockData && (
        <>
          <div className="text-lg text-yellow-400 mb-6">
            Time Left: {Math.floor(timeLeft / 60)}:
            {String(timeLeft % 60).padStart(2, "0")}
          </div>

          {mockData.questions.map((q, index) => (
            <div
              key={q.id}
              className="bg-black/60 p-6 rounded-xl border border-white/10 mb-6"
            >
              <p>
                Q{index + 1}. {q.question}
              </p>

              {q.options.map((option) => (
                <label key={option} className="block mt-2">
                  <input
                    type="radio"
                    name={`q${q.id}`}
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

      {/* ---------- RESULT ---------- */}
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