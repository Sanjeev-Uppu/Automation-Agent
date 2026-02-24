import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import jsPDF from "jspdf";

export default function PlannerPage() {

  const [grade, setGrade] = useState("");
  const [subject, setSubject] = useState("");
  const [chapter, setChapter] = useState("");
  const [days, setDays] = useState(7);

  const [grades, setGrades] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [chapters, setChapters] = useState([]);

  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(false);

  // ---------------- FETCH GRADES ----------------
  useEffect(() => {
    fetch("http://127.0.0.1:8002/grades")
      .then(res => res.json())
      .then(data => setGrades(data));
  }, []);

  // ---------------- FETCH SUBJECTS ----------------
  useEffect(() => {
    if (!grade) return;

    fetch(`http://127.0.0.1:8002/subjects?grade=${grade}`)
      .then(res => res.json())
      .then(data => setSubjects(data));
  }, [grade]);

  // ---------------- FETCH CHAPTERS ----------------
  useEffect(() => {
    if (!grade || !subject) return;

    fetch(`http://127.0.0.1:8002/chapters?grade=${grade}&subject=${subject}`)
      .then(res => res.json())
      .then(data => setChapters(data));
  }, [grade, subject]);

  // ---------------- GENERATE PLAN ----------------
  const generatePlan = async () => {

    if (!grade || !subject || !chapter || !days) {
      alert("Please select all fields");
      return;
    }

    setLoading(true);

    const response = await fetch(
      "http://127.0.0.1:8002/generate-plan/",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          grade: parseInt(grade),
          subject,
          chapter_name: chapter,
          duration_days: parseInt(days)
        })
      }
    );

    const data = await response.json();
    setPlan(data);
    setLoading(false);
  };

  // ---------------- DOWNLOAD PDF ----------------
  const downloadPDF = () => {

    if (!plan) return;

    const pdf = new jsPDF();
    let y = 20;

    pdf.setFontSize(18);
    pdf.text("AI Study Plan", 105, y, { align: "center" });
    y += 10;

    pdf.setFontSize(12);
    pdf.text(`Grade: ${grade}`, 15, y); y += 6;
    pdf.text(`Subject: ${subject}`, 15, y); y += 6;
    pdf.text(`Chapter: ${chapter}`, 15, y); y += 10;

    plan.plan.forEach(dayItem => {

      pdf.setFontSize(14);
      pdf.text(`Day ${dayItem.day} – ${dayItem.focus}`, 15, y);
      y += 7;

      pdf.setFontSize(11);
      pdf.text(`Estimated Time: ${dayItem.estimated_hours} hrs`, 15, y);
      y += 7;

      dayItem.topics.forEach(topic => {
        pdf.text(`• ${topic}`, 20, y);
        y += 6;
      });

      y += 4;
    });

    pdf.save("AI_Study_Plan.pdf");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-slate-900 to-purple-950 text-white p-8">

      <h1 className="text-4xl font-bold mb-8">
        AI Smart Study Planner
      </h1>

      {/* CONTROLS */}
      <div className="grid md:grid-cols-4 gap-4 mb-8">

        <select
          value={grade}
          onChange={(e) => setGrade(e.target.value)}
          className="bg-black p-3 rounded border border-gray-600"
        >
          <option value="">Select Grade</option>
          {grades.map(g => (
            <option key={g} value={g}>{g}</option>
          ))}
        </select>

        <select
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
          className="bg-black p-3 rounded border border-gray-600"
        >
          <option value="">Select Subject</option>
          {subjects.map(s => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>

        <select
          value={chapter}
          onChange={(e) => setChapter(e.target.value)}
          className="bg-black p-3 rounded border border-gray-600"
        >
          <option value="">Select Chapter</option>
          {chapters.map(c => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>

        <input
          type="number"
          value={days}
          onChange={(e) => setDays(e.target.value)}
          className="bg-black p-3 rounded border border-gray-600"
        />

      </div>

      <motion.button
        whileHover={{ scale: 1.05 }}
        onClick={generatePlan}
        className="bg-gradient-to-r from-pink-500 via-cyan-500 to-green-400 px-6 py-3 rounded-xl font-bold"
      >
        {loading ? "Generating..." : "Generate Plan"}
      </motion.button>

      {/* PLAN DISPLAY */}
      {plan && (
        <div className="mt-10 space-y-6">

          {plan.plan.map(dayItem => (
            <div key={dayItem.day} className="bg-white/10 p-6 rounded-xl">
              <h2 className="font-bold">
                Day {dayItem.day} – {dayItem.focus}
              </h2>
              <p className="text-sm text-gray-300">
                {dayItem.estimated_hours} hrs
              </p>
            </div>
          ))}

          <button
            onClick={downloadPDF}
            className="mt-6 bg-yellow-500 px-6 py-2 rounded font-bold"
          >
            Download PDF
          </button>

        </div>
      )}

    </div>
  );
}