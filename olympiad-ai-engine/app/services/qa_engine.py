import os
from google import genai
from google.genai.errors import ClientError


def generate_answer(context, question):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "API key not configured."

    # 🔥 LIMIT CONTEXT SIZE (Prevents token overflow crash)
    MAX_CONTEXT_CHARS = 4000
    context = context[:MAX_CONTEXT_CHARS]

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

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if not response.text:
            return "AI returned empty response."

        return response.text.strip()

    except ClientError:
        return "AI quota exceeded. Please try again later."

    except Exception as e:
        print("LLM Error:", str(e))
        return "AI service temporarily unavailable."
