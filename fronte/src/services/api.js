const BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8002";

export const api = {
  get: async (endpoint) => {
    const res = await fetch(`${BASE_URL}${endpoint}`);
    if (!res.ok) throw new Error("API error");
    return res.json();
  },

  post: async (endpoint, body) => {
    const res = await fetch(`${BASE_URL}${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error("API error");
    return res.json();
  },
};