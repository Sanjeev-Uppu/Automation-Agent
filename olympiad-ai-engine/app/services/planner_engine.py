import os
import json
from google import genai

def generate_llm_plan(duration_days: int, chapter_name: str):

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise Exception("GEMINI_API_KEY not found")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an academic curriculum planner.

Create a structured and professional {duration_days}-day study plan
for the chapter "{chapter_name}".

Requirements:
- Distribute topics evenly
- Include 1 revision day
- Include 1 mock practice day
- Make tasks clear and actionable
- Keep it structured and balanced
- Return ONLY valid JSON

JSON Format:

{{
  "duration_days": {duration_days},
  "chapter": "{chapter_name}",
  "plan": [
    {{
      "day": 1,
      "focus": "Main topic",
      "topics": ["Topic 1", "Topic 2"],
      "tasks": ["Read", "Practice MCQs", "Revise Notes"],
      "estimated_hours": 2
    }}
  ]
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={"response_mime_type": "application/json"}
    )

    if not response.text:
        raise Exception("Empty LLM response")

    return json.loads(response.text)
