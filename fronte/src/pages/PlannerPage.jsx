import { useState } from "react";

export default function PlannerPage() {
  const [days, setDays] = useState(7);
  const [plan, setPlan] = useState(null);

  const generatePlan = async () => {
    const response = await fetch(
      `http://127.0.0.1:8002/generate-plan/?duration_days=${days}&chapter_name=Animals`,
      { method: "POST" }
    );

    const data = await response.json();
    setPlan(data);
  };

  const downloadPDF = () => {
    window.print();
  };

  return (
    <div className="p-8 text-white">
      <h1 className="text-3xl font-bold mb-6">Study Planner</h1>

      <div className="flex gap-4 mb-6">
        <input
          type="number"
          value={days}
          onChange={(e) => setDays(e.target.value)}
          className="bg-gray-800 p-2 rounded"
        />
        <button
          onClick={generatePlan}
          className="bg-cyan-600 px-4 py-2 rounded"
        >
          Generate Plan
        </button>
      </div>

      {plan && (
        <>
          <table className="w-full border border-gray-700 text-left">
            <thead className="bg-gray-800">
              <tr>
                <th className="p-3 border">Day</th>
                <th className="p-3 border">Topics</th>
                <th className="p-3 border">Tasks</th>
              </tr>
            </thead>
            <tbody>
              {plan.plan.map((item) => (
                <tr key={item.day} className="border">
                  <td className="p-3 border">{item.day}</td>
                  <td className="p-3 border">{item.topics}</td>
                  <td className="p-3 border">{item.tasks}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <button
            onClick={downloadPDF}
            className="mt-6 bg-purple-600 px-6 py-2 rounded"
          >
            Download as PDF
          </button>
        </>
      )}
    </div>
  );
}
