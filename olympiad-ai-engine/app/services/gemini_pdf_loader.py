import os
import pdfplumber
import time
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def load_pdf(file_path: str):

    print(f"\n📄 Processing: {file_path}")

    # -----------------------------
    # 1️⃣ Try pdfplumber (Primary)
    # -----------------------------
    try:
        full_text = ""

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                full_text += text + "\n"

        if full_text.strip() and len(full_text.strip()) > 250:
            print("✅ Extracted using pdfplumber")
            return full_text
        else:
            print("⚠️ pdfplumber extraction low/empty")

    except Exception as e:
        print("❌ pdfplumber failed:", e)

    # -----------------------------
    # 2️⃣ Fallback to Gemini AI
    # -----------------------------
    try:
        print("🚀 Falling back to Gemini AI extraction...")

        uploaded_file = genai.upload_file(
            path=file_path,
            display_name=os.path.basename(file_path)
        )

        while uploaded_file.state.name == "PROCESSING":
            time.sleep(2)
            uploaded_file = genai.get_file(uploaded_file.name)

        if uploaded_file.state.name == "FAILED":
            raise Exception("Gemini PDF processing failed.")

        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = """
        Extract ALL readable text from this PDF.
        Do not summarize.
        Do not skip anything.
        Maintain structure.
        Return plaintext only.
        """

        response = model.generate_content([prompt, uploaded_file])

        print("✅ Extracted using Gemini AI")
        return response.text

    except Exception as e:
        print("❌ Gemini extraction failed:", e)

    raise Exception("❌ All extraction methods failed.")