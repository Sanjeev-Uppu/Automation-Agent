import os
from google import genai


def generate_answer(context, question):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Check your .env file.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You must answer ONLY from the provided context.
If the answer is not in the context, say:
"Answer not found in lesson."

Context:
{context}

Question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text
