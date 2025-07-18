# src/summariser.py
import os
from dotenv import load_dotenv
from openai import OpenAI  # new 1.x client

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM = "You are a concise, professional lamb‑market analyst."

def summarise(prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user",   "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"⚠️ OpenAI API error: {e}")
        return "_[Summary unavailable]_"
