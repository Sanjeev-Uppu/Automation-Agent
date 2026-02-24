import os
import json
import re
from google import genai
from google.genai.errors import ClientError


def generate_question_paper_llm(
    context,
    chapter_name,
    num_questions,
    duration_minutes,
    grade,
    subject,
    marks_per_question,
    difficulty_level
):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise Exception("API key not configured.")

    context = context[:4000]

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an AI School Question Paper Generator.

Generate a structured school exam paper.

School Name: AiSmartLive Olympiad School
Grade: {grade}
Subject: {subject}
Chapter: {chapter_name}

Number of Questions: {num_questions}
Marks per Question: {marks_per_question}
Total Duration: {duration_minutes} minutes
Difficulty Level: {difficulty_level}

Instructions:
- All questions compulsory
- Each question carries {marks_per_question} marks
- Maintain {difficulty_level} level
- Strict academic tone
- Multiple Choice Questions only
- Provide Answer Key at end
- Do NOT include explanation
- Do NOT include markdown
- Output ONLY valid JSON

Return STRICT JSON format only:

{{
    "school_name": "AiSmartLive Olympiad School",
    "grade": {grade},
    "subject": "{subject}",
    "chapter": "{chapter_name}",
    "difficulty_level": "{difficulty_level}",
    "duration_minutes": {duration_minutes},
    "marks_per_question": {marks_per_question},
    "questions": [
        {{
            "id": 1,
            "question": "...",
            "options": ["A", "B", "C", "D"],
            "correct_answer": "..."
        }}
    ]
}}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if not response.text:
            raise Exception("Empty response from Gemini")

        text = response.text.strip()

        # 🔥 PRODUCTION SAFE JSON EXTRACTION
        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if not json_match:
            raise Exception("No valid JSON found in Gemini response")

        clean_json = json_match.group()

        return json.loads(clean_json)

    except ClientError:
        raise Exception("Gemini quota exceeded")

    except Exception as e:
        print("Question Paper LLM Error:", str(e))
        raise Exception("Failed to generate question paper.")