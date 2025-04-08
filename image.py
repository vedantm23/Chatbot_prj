import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, image):
    model = genai.GenerativeModel("gemini-1.5-pro")
    if input_text.strip():
        response = model.generate_content([input_text, image])
    else:
        response = model.generate_content([image])
    return response.text
