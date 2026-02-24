import os
import json
import re
import random
from google import genai


# ==============================
# 🔥 LLM MOCK GENERATOR
# ==============================
def generate_mock_exam_llm(
    context,
    chapter_name,
    num_questions,
    duration_minutes,
    grade,
    subject
):

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise Exception("GEMINI_API_KEY not found")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an Olympiad Exam Paper Generator.

Generate {num_questions} multiple choice questions strictly from the lesson context.

Rules:
- Exactly 4 options per question
- Only one correct answer
- No explanations
- Return ONLY valid JSON

JSON FORMAT:

{{
  "intent": "mock_exam",
  "grade": {grade},
  "subject": "{subject}",
  "chapter": "{chapter_name}",
  "duration_minutes": {duration_minutes},
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
        contents=prompt,
        config={"response_mime_type": "application/json"}
    )

    if not response.text:
        raise Exception("Empty LLM response")

    try:
        return json.loads(response.text)

    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", response.text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise Exception("Invalid JSON returned")
        

# ==============================
# 🧠 FALLBACK GENERATOR
# ==============================
def generate_fallback_mock(
    chapter_name,
    num_questions,
    duration_minutes,
    grade,
    subject
):

    sample_pool = [
        {
            "question": "Which of the following is correct?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": "Option A"
        }
        for _ in range(50)
    ]

    questions = []

    for i in range(num_questions):
        q = sample_pool[i % len(sample_pool)]
        questions.append({
            "id": i + 1,
            "question": q["question"],
            "options": q["options"],
            "correct_answer": q["correct_answer"]
        })

    return {
        "intent": "mock_exam",
        "grade": grade,
        "subject": subject,
        "chapter": chapter_name,
        "duration_minutes": duration_minutes,
        "questions": questions
    }