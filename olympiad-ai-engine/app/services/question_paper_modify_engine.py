import os
import json
from google import genai
import google.generativeai as genai
from google.genai.errors import ClientError


def regenerate_question_paper_with_modifications(
    original_paper: dict,
    modification_request: str
):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise Exception("API key not configured.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an AI School Question Paper Modifier.

You are given an existing question paper in JSON format.

Your task:
Modify the paper strictly according to the modification request.

RULES:
- Do NOT change grade, subject, chapter unless explicitly asked.
- Maintain valid JSON format.
- Keep same structure.
- Return ONLY valid JSON.
- No markdown.
- No explanation.

Original Question Paper:
{json.dumps(original_paper, indent=2)}

Modification Request:
{modification_request}

Return STRICT JSON only.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        start = text.find("{")
        end = text.rfind("}") + 1
        clean_json = text[start:end]

        return json.loads(clean_json)

    except ClientError:
        raise Exception("Gemini quota exceeded.")

    except Exception as e:
        print("Modification Error:", str(e))
        raise Exception("Failed to modify question paper.")