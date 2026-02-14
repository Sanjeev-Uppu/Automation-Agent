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

  // TIMER LOGIC
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
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(submission),
      }
    );

    const data = await response.json();
    setResult(data);
  };

  if (!mockData) {
    return (
      <div className="text-white text-center mt-10">
        No Mock Test Available
      </div>
    );
  }

  return (
    <div className="space-y-6 bg-white/5 backdrop-blur-xl p-8 rounded-3xl border border-white/10">

      <h2 className="text-2xl font-bold text-cyan-400">
        {mockData.chapter} Mock Test
      </h2>

      {!started && (
        <button
          onClick={() => setStarted(true)}
          className="px-6 py-3 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-xl"
        >
          Start Test
        </button>
      )}

      {started && !result && (
        <>
          <div className="text-lg text-yellow-400">
            Time Left: {Math.floor(timeLeft / 60)}:
            {String(timeLeft % 60).padStart(2, "0")}
          </div>

          {mockData.questions.map((q) => (
            <div
              key={q.id}
              className="bg-black/60 p-6 rounded-xl border border-white/10 space-y-3"
            >
              <p className="font-semibold">
                {q.id}. {q.question}
              </p>

              {q.options.map((option) => (
                <label key={option} className="block cursor-pointer">
                  <input
                    type="radio"
                    name={`q${q.id}`}
                    value={option}
                    onChange={() =>
                      handleSelect(q.id, option)
                    }
                    className="mr-2"
                  />
                  {option}
                </label>
              ))}
            </div>
          ))}

          <button
            onClick={handleSubmit}
            className="px-6 py-3 bg-green-600 rounded-xl mt-4"
          >
            Submit Test
          </button>
        </>
      )}

      {result && (
        <div className="bg-black/70 p-6 rounded-xl border border-white/10 space-y-2">
          <h3 className="text-xl font-bold text-green-400">
            Test Completed
          </h3>
          <p>Total Questions: {result.total_questions}</p>
          <p>Correct Answers: {result.correct}</p>
          <p>Score: {result.percentage}%</p>
        </div>
      )}
    </div>
  );
}
