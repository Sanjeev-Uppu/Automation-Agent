import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function HomePage() {
  const [grade, setGrade] = useState("");
  const [subject, setSubject] = useState("");
  const [chapter, setChapter] = useState("");

  const [grades, setGrades] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [chapters, setChapters] = useState([]);

  const navigate = useNavigate();

  // Load grades
  useEffect(() => {
    fetch("http://127.0.0.1:8002/grades")
      .then((res) => res.json())
      .then((data) => setGrades(data));
  }, []);

  // Load subjects when grade changes
  useEffect(() => {
    if (!grade) return;

    fetch(`http://127.0.0.1:8002/subjects?grade=${grade}`)
      .then((res) => res.json())
      .then((data) => setSubjects(data));
  }, [grade]);

  // Load chapters when subject changes
  useEffect(() => {
    if (!grade || !subject) return;

    fetch(
      `http://127.0.0.1:8002/chapters?grade=${grade}&subject=${subject}`
    )
      .then((res) => res.json())
      .then((data) => setChapters(data));
  }, [subject]);

  const openChat = () => {
    navigate("/chat", {
      state: {
        grade,
        subject,
        chapter_name: chapter || null,
      },
    });
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-black via-indigo-950 to-purple-950 text-white p-10">

      <div className="bg-white/5 backdrop-blur-xl p-10 rounded-3xl border border-white/10 shadow-2xl w-full max-w-2xl">

        <h1 className="text-4xl font-bold mb-6 text-cyan-400">
          Olympiad AI Learning Hub
        </h1>

        {/* Grade */}
        <select
          value={grade}
          onChange={(e) => {
            setGrade(e.target.value);
            setSubject("");
            setChapter("");
          }}
          className="w-full mb-4 p-3 rounded-xl bg-black/60 border border-white/10"
        >
          <option value="">Select Grade</option>
          {grades.map((g) => (
            <option key={g} value={g}>
              Grade {g}
            </option>
          ))}
        </select>

        {/* Subject */}
        <select
          value={subject}
          onChange={(e) => {
            setSubject(e.target.value);
            setChapter("");
          }}
          disabled={!grade}
          className="w-full mb-4 p-3 rounded-xl bg-black/60 border border-white/10"
        >
          <option value="">Select Subject</option>
          {subjects.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>

        {/* Chapter */}
        <select
          value={chapter}
          onChange={(e) => setChapter(e.target.value)}
          disabled={!subject}
          className="w-full mb-6 p-3 rounded-xl bg-black/60 border border-white/10"
        >
          <option value="">All Chapters</option>
          {chapters.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>

        <button
          onClick={openChat}
          disabled={!grade || !subject}
          className="w-full py-4 rounded-xl bg-gradient-to-r from-cyan-500 to-purple-600 hover:scale-105 transition shadow-lg font-semibold"
        >
          Open Chat
        </button>

      </div>
    </div>
  );
}
