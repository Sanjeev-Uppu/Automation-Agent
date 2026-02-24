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
You are an AI Olympiad Academic Assistant specialized in Mathematics, Science, Logical Reasoning, and English Olympiads for Classes 1–12.

INSTRUCTIONS:

1. Always prioritize answering strictly based on the provided Olympiad context.
2. If the answer exists in the context, use only that information.
3. If context is insufficient:
   - Use standard Olympiad-level syllabus knowledge.
   - Maintain Olympiad difficulty and clarity.
4. Provide:
   - Clear explanation
   - Step-by-step solution (for numerical questions)
   - Key concept used
   - Short trick (if applicable)
5. Do not generate unrelated or general conversational answers.
6. If the question is illegal, harmful, or unrelated to academics, respond with:
   "please ask me subject relevant questions only"
7. Keep the tone student-friendly and exam-oriented.
8. If syllabus mapping is possible, mention:
   (Class – Subject – Chapter){context}

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
