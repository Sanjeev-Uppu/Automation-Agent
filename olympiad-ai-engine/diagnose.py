import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

print("API KEY:", os.getenv("GEMINI_API_KEY")[:10], "...")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Listing models...")

for model in client.models.list():
    print(model.name)
