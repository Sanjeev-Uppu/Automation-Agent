import os
from google import genai

_api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=_api_key)


def generate_questions(context: str, difficulty: str, count: int = 5):

    prompt = f"""
You are an Olympiad Question Generator.

Generate {count} {difficulty} level MCQs.

STRICT RULES:
- Use ONLY the provided context.
- 4 options per question.
- Mark correct answer clearly.
- Provide short explanation.
- If insufficient data, say:
  "Not enough information in lesson."

Context:
{context}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text
