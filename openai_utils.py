
import openai
import os

# Load API key
openai.api_key = os.getenv("") or ""

# For OpenAI v1.0+ SDK
client = openai.OpenAI()

def generate_gpt_nudge(bias, behavior, context=None):
    prompt = f"""
You are a behavioral finance coach.
A user showed a behavior that reflects {bias}.

Behavior pattern: {behavior}
Context: {context if context else 'N/A'}

Write a short, thoughtful nudge that helps the user reflect on this pattern.
Be emotionally intelligent and conversational.
Limit to 1–2 sentences.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a behavioral finance expert helping users reflect on their financial habits."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=100,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[OpenAI error: {e}]"
