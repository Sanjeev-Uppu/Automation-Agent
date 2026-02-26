const BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function askQuestion(payload) {
  const response = await fetch(`${BASE_URL}/ask/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error("Failed to fetch answer");
  }

  return await response.json();
}