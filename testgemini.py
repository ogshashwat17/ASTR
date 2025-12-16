from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print("API key loaded:", bool(api_key))

genai.configure(api_key=api_key)

# ✅ THIS IS THE ONLY WORKING MODEL FOR YOUR SDK + v1beta
model = genai.GenerativeModel("models/gemini-pro")

response = model.generate_content("Say hello")
print(response.text)
