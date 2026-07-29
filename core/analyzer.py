import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize model
model = genai.GenerativeModel("gemini-1.5-pro")


def clean_json(text: str):
    """
    Cleans Gemini response and parses JSON safely
    """
    text = re.sub(r"```json|```", "", text).strip()
    return json.loads(text)


def analyze_email(text: str):
    prompt = f"""
You are an expert email classifier for job applications.

Return ONLY valid JSON.
No markdown.
No explanation.

Schema:
{{
  "is_job_related": boolean,
  "category": "interview" | "rejection" | "other",
  "company": string,
  "date": string,
  "summary": string
}}

Rules:
- Be precise and factual
- Do not hallucinate
- If information is missing → "unknown"
- Summary must be 1–2 sentences max

Definitions:
- "interview" → invitation or next steps
- "rejection" → decline or not selected
- "other" → unclear or neutral

Email:
{text}
"""

    response = model.generate_content(prompt)

    try:
        return clean_json(response.text)
    except Exception:
        return {
            "is_job_related": False,
            "category": "other",
            "company": "unknown",
            "date": "unknown",
            "summary": "Failed to parse response"
        }