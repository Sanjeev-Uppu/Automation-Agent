import os
from google import genai

def generate_mock_exam(context, chapter_name):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise Exception("GEMINI_API_KEY not found")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an Olympiad Exam Paper Generator.

Generate 10 MCQs strictly from the lesson context.

Requirements:
- Exactly 4 options per question
- Only one correct answer
- Mix difficulty levels
- No explanations
- Return ONLY valid JSON

JSON format:

{{
  "intent": "mock_exam",
  "chapter": "{chapter_name}",
  "duration_minutes": 15,
  "questions": [
    {{
      "id": 1,
      "question": "Question text",
      "options": ["A", "B", "C", "D"],
      "correct_answer": "Correct option text"
    }}
  ]
}}

Context:
{context}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    # Remove markdown if Gemini wraps JSON
    if text.startswith("```"):
        text = text.split("```")[1]

    return text
