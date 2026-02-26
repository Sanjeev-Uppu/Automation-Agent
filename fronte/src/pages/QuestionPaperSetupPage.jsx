import { api } from "../services/api";
import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

export default function QuestionPaperSetupPage() {

  const location = useLocation();
  const navigate = useNavigate();

  const { grade, subject, chapter_name } = location.state || {};

  const [numberOfQuestions, setNumberOfQuestions] = useState("");
  const [marksPerQuestion, setMarksPerQuestion] = useState("");
  const [durationMinutes, setDurationMinutes] = useState("");
  const [difficulty, setDifficulty] = useState("");
  const [loading, setLoading] = useState(false);

  if (!grade || !subject) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-black text-white">
        Please select grade and subject first.
      </div>
    );
  }

  const handleGenerate = async () => {

    if (!numberOfQuestions || !marksPerQuestion || !durationMinutes || !difficulty) {
      alert("Please fill all fields");
      return;
    }

    try {
      setLoading(true);

      const data = await api.post("/generate-question-paper/", {
        grade,
        subject,
        chapter_name,
        number_of_questions: parseInt(numberOfQuestions),
        marks_per_question: parseInt(marksPerQuestion),
        duration_minutes: parseInt(durationMinutes),
        difficulty_level: difficulty
      });

      if (data.paper_data) {
        navigate("/question-paper-preview", {
          state: {
            paper_data: data.paper_data
          }
        });
      } else {
        alert("Failed to generate question paper.");
      }

    } catch (error) {
      console.error("Generation failed:", error);
      alert("Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white flex justify-center items-center">

      <div className="bg-gray-900 p-8 rounded-xl w-96 space-y-4">

        <h2 className="text-2xl font-bold text-center">
          Configure Question Paper
        </h2>

        <input
          type="number"
          placeholder="Number of Questions"
          value={numberOfQuestions}
          onChange={(e) => setNumberOfQuestions(e.target.value)}
          className="w-full p-2 bg-black border border-gray-600 rounded"
        />

        <input
          type="number"
          placeholder="Marks per Question"
          value={marksPerQuestion}
          onChange={(e) => setMarksPerQuestion(e.target.value)}
          className="w-full p-2 bg-black border border-gray-600 rounded"
        />

        <input
          type="number"
          placeholder="Duration (Minutes)"
          value={durationMinutes}
          onChange={(e) => setDurationMinutes(e.target.value)}
          className="w-full p-2 bg-black border border-gray-600 rounded"
        />

        <select
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
          className="w-full p-2 bg-black border border-gray-600 rounded"
        >
          <option value="">Select Difficulty</option>
          <option value="Easy">Easy</option>
          <option value="Medium">Medium</option>
          <option value="Hard">Hard</option>
        </select>

        <button
          onClick={handleGenerate}
          disabled={loading}
          className="w-full bg-cyan-600 p-2 rounded"
        >
          {loading ? "Generating..." : "Generate Question Paper"}
        </button>

      </div>
    </div>
  );
}