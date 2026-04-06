import os
from groq import Groq
import json

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

def generate_problem_content(title, topic, difficulty, language_a="python", language_b="java"):
    prompt = f"""
You are a DSA teaching assistant. For the problem "{title}" (Topic: {topic}, Difficulty: {difficulty}), generate the following in JSON format only, no markdown, no explanation outside JSON:

{{
  "pattern_name": "name of the algorithmic pattern",
  "pattern_explanation": "2-3 sentence explanation of the pattern and why it applies here",
  "time_complexity": "O(...)",
  "space_complexity": "O(...)",
  "python_template": "complete Python code template with comments explaining each step",
  "java_template": "complete Java code template with comments explaining each step"
}}

Make the code templates educational — include comments that explain the thinking, not just the syntax.
Return only valid JSON. No backticks. No extra text.
"""
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-70b-8192",
        )
        text = chat_completion.choices[0].message.content.strip()
        # Clean up any potential markdown formatting in case Claude still outputs it
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())
    except Exception:
        return {}
