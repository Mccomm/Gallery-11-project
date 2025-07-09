import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # ✅ Load .env before using getenv

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("❌ OPENAI_API_KEY not found in environment.")

client = OpenAI(api_key=api_key)

def get_chatgpt_reply(prompt, system_prompt=""):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
