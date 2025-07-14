from openai import OpenAI

client = OpenAI()

SYSTEM = "You are a concise professional lamb-market analyst. Always reference numbers in your answer."

def summarise(prompt: str) -> str:
    chat = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user",   "content": prompt}
        ],
        temperature=0.3,
        max_tokens=300,
    )
    return chat.choices[0].message.content.strip()
