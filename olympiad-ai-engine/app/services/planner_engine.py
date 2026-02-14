import os
import json
from google import genai


def generate_llm_plan(duration_days, chapter_name):

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise Exception("No API key found")

    client = genai.Client(api_key=api_key)

    prompt = f"""
Create a structured study plan for {duration_days} days
for the chapter "{chapter_name}".

Requirements:
- Divide topics evenly
- Include revision days
- Include mock practice days
- Return ONLY valid JSON

Format:

{{
  "duration_days": {duration_days},
  "chapter": "{chapter_name}",
  "plan": [
    {{
      "day": 1,
      "topics": "Topics to study",
      "tasks": "Reading / Practice / Revision"
    }}
  ]
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.split("```")[1]

    return text
