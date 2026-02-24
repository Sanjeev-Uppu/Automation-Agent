import os
import json
from google import genai

def generate_llm_plan(duration_days, chapter_name, grade, subject):

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise Exception("GEMINI_API_KEY not found")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an AI Academic Study Planner.

Grade: {grade}
Subject: {subject}
Chapter: {chapter_name}
Duration: {duration_days} days

Create a structured study plan.

Return STRICT JSON format only:

{{
    "plan": [
        {{
            "day": 1,
            "focus": "Main concept for the day",
            "estimated_hours": 2,
            "topics": ["Topic 1", "Topic 2"],
            "tasks": ["Task 1", "Task 2"]
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
