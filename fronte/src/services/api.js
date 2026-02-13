const BASE_URL = "http://127.0.0.1:8002";

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
