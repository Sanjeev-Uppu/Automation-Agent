import { useState, useRef } from "react";
import html2canvas from "html2canvas";
import jsPDF from "jspdf";

export default function PlannerPage() {
  const [days, setDays] = useState(7);
  const [chapter, setChapter] = useState("Animals");
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(false);

  const plannerRef = useRef(null);

  const generatePlan = async () => {
    setLoading(true);

    const response = await fetch(
      `http://127.0.0.1:8002/generate-plan/?duration_days=${days}&chapter_name=${chapter}`,
      { method: "POST" }
    );

    const data = await response.json();
    setPlan(data);
    setLoading(false);
  };

  // ✅ PDF Download Function
  const downloadPDF = async () => {
  if (!plannerRef.current) return;

  try {
    // 🔥 Temporarily remove gradient background
    const originalBg = document.body.style.background;
    document.body.style.background = "#ffffff";

    const canvas = await html2canvas(plannerRef.current, {
      scale: 2,
      useCORS: true,
      backgroundColor: "#ffffff",
    });

    const imgData = canvas.toDataURL("image/png");

    const pdf = new jsPDF("p", "mm", "a4");

    const pageWidth = 210;
    const pageHeight = 297;

    const imgWidth = pageWidth;
    const imgHeight = (canvas.height * imgWidth) / canvas.width;

    let heightLeft = imgHeight;
    let position = 0;

    pdf.addImage(imgData, "PNG", 0, position, imgWidth, imgHeight);
    heightLeft -= pageHeight;

    while (heightLeft > 0) {
      position = heightLeft - imgHeight;
      pdf.addPage();
      pdf.addImage(imgData, "PNG", 0, position, imgWidth, imgHeight);
      heightLeft -= pageHeight;
    }

    pdf.save("AI_Study_Plan.pdf");

    // 🔥 Restore background
    document.body.style.background = originalBg;

  } catch (error) {
    console.error("PDF error:", error);
  }
};




  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-indigo-950 to-purple-950 text-white p-10">

      <div className="max-w-5xl mx-auto">

        {/* HEADER */}
        <h1 className="text-4xl font-bold mb-2">AI Study Planner</h1>
        <p className="text-gray-400 mb-8">
          Generate a structured and optimized study roadmap.
        </p>

        {/* CONTROLS */}
        <div className="bg-gray-900 p-6 rounded-2xl shadow-lg flex gap-4 mb-10">
          <input
            type="number"
            value={days}
            onChange={(e) => setDays(e.target.value)}
            className="bg-gray-800 p-3 rounded-lg w-32 outline-none"
            placeholder="Days"
          />

          <input
            type="text"
            value={chapter}
            onChange={(e) => setChapter(e.target.value)}
            className="bg-gray-800 p-3 rounded-lg flex-1 outline-none"
            placeholder="Chapter Name"
          />

          <button
            onClick={generatePlan}
            className="bg-cyan-600 hover:bg-cyan-500 transition px-6 py-3 rounded-lg font-semibold"
          >
            {loading ? "Generating..." : "Generate Plan"}
          </button>
        </div>

        {/* PLAN CARDS */}
        {plan && (
          <div ref={plannerRef} className="space-y-6">
            {plan.plan.map((dayItem) => (
              <div
                key={dayItem.day}
                className="bg-gray-900 rounded-2xl p-6 shadow-lg hover:scale-[1.01] transition"
              >
                <div className="flex justify-between items-center mb-3">
                  <h2 className="text-xl font-bold">
                    Day {dayItem.day} – {dayItem.focus}
                  </h2>
                  <span className="text-sm bg-purple-700 px-3 py-1 rounded-full">
                    {dayItem.estimated_hours} hrs
                  </span>
                </div>

                <div className="mb-3">
                  <h3 className="text-cyan-400 font-semibold mb-1">Topics</h3>
                  <ul className="list-disc list-inside text-gray-300">
                    {dayItem.topics.map((topic, index) => (
                      <li key={index}>{topic}</li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h3 className="text-green-400 font-semibold mb-1">Tasks</h3>
                  <ul className="list-disc list-inside text-gray-300">
                    {dayItem.tasks.map((task, index) => (
                      <li key={index}>{task}</li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* ✅ ONLY ADDED BUTTON */}
        {plan && (
          <div className="flex justify-center mt-12">
            <button
              onClick={downloadPDF}
              className="bg-gradient-to-r from-purple-600 to-pink-600 hover:scale-105 transition px-10 py-4 rounded-2xl text-lg font-semibold shadow-xl"
            >
              Download as PDF
            </button>
          </div>
        )}

      </div>
    </div>
  );
}
