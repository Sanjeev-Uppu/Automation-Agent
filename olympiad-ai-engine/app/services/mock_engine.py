import os
import json
import re
import random
from fastapi import FastAPI
from google import genai

app = FastAPI()


# ==============================
# 🔥 LLM MOCK GENERATOR
# ==============================
def generate_mock_exam_llm(context, chapter_name):

    print("\n===== LLM EXECUTION STARTED =====")

    api_key = os.getenv("GEMINI_API_KEY")
    print("API KEY FOUND:", bool(api_key))

    if not api_key:
        raise Exception("GEMINI_API_KEY not found in environment")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an Olympiad Exam Paper Generator.

Generate 5 MCQs strictly from the lesson context.

Requirements:
- Exactly 4 options per question
- Only one correct answer
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

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )

        print("LLM RAW RESPONSE OBJECT:", response)

        if not response.text:
            raise Exception("LLM returned EMPTY response")

        print("LLM RAW TEXT:\n", response.text)

        # Try parsing JSON
        try:
            parsed_json = json.loads(response.text)
            print("✅ JSON PARSED SUCCESSFULLY")
            return parsed_json

        except json.JSONDecodeError as e:
            print("❌ JSON PARSE ERROR:", str(e))

            # Try extracting JSON manually
            match = re.search(r"\{.*\}", response.text, re.DOTALL)
            if match:
                print("Attempting manual JSON extraction...")
                return json.loads(match.group(0))
            else:
                raise Exception("No valid JSON found in response")

    except Exception as e:
        print("🚨 LLM FAILURE:", str(e))
        raise


# ==============================
# 🧠 FALLBACK ENGINE
# ==============================
def generate_mock_exam_fallback(chapter_name):

    print("⚠️ USING FALLBACK ENGINE")

    sample_questions = [
        {
            "id": 1,
            "question": "Which of the following is a mammal?",
            "options": ["Frog", "Whale", "Snake", "Crocodile"],
            "correct_answer": "Whale"
        },
        {
            "id": 2,
            "question": "Which animal lays eggs?",
            "options": ["Cow", "Goat", "Hen", "Dog"],
            "correct_answer": "Hen"
        },
        {
            "id": 3,
            "question": "Which animal undergoes metamorphosis?",
            "options": ["Frog", "Cow", "Dog", "Cat"],
            "correct_answer": "Frog"
        },
        {
            "id": 4,
            "question": "Which is an aquatic animal?",
            "options": ["Camel", "Whale", "Tiger", "Monkey"],
            "correct_answer": "Whale"
        },
        {
            "id": 5,
            "question": "Which animal gives birth to young ones?",
            "options": ["Snake", "Hen", "Cow", "Frog"],
            "correct_answer": "Cow"
        }
    ]

    random.shuffle(sample_questions)

    return {
        "intent": "mock_exam",
        "chapter": chapter_name,
        "duration_minutes": 15,
        "questions": sample_questions
    }


# ==============================
# 🚀 FASTAPI ROUTE
# ==============================
@app.post("/generate-mock/")
async def generate_mock():

    context = "Animals are living organisms. Mammals give birth to young ones..."
    chapter_name = "Animals"

    try:
        result = generate_mock_exam_llm(context, chapter_name)
        print("✅ LLM SUCCESS")
        return result

    except Exception as e:
        print("⚠️ LLM FAILED. Switching to fallback.")
        print("ERROR DETAILS:", str(e))
        return generate_mock_exam_fallback(chapter_name)
