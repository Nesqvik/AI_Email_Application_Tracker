import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv
from model.EmailAnalysis import EmailAnalysis
from langsmith import traceable, trace
import logging


# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize model
model = genai.GenerativeModel("models/gemini-3.1-flash-lite")


#PRINT ALL AVAILABLE MODELS
for m in genai.list_models():
    print(m.name, m.supported_generation_methods)

def clean_json(text: str):
    """
    Cleans Gemini response and parses JSON safely
    """
    text = re.sub(r"```json|```", "", text).strip()
    return json.loads(text)

@traceable(
    name="analyze_email_pipeline",
    metadata={"component": "email_classifier"}
)
def analyze_email(text: str):

    prompt = f"""
You are an expert email classifier for job applications.

Return ONLY valid JSON.
No markdown.
No explanation.

Schema:
{{
  "is_job_related": boolean,
  "category": "interview_invitation" | "interview_followup" | "rejection" | "offer" | "application_received" | "assessment" | "networking" | "other_job_related" | "not_job_related",
  "company": string,
  "date": string,
  "summary": string,
  "confidence": number,
  "language": "en" | "de" | "other"
}}

Email:
{text}
"""

    for attempt in range(2):

        with trace(
            name="retry_attempt",
            metadata={"attempt": attempt}
        ):
            response = call_llm(prompt, attempt)

            logging.info(f"[Attempt {attempt}] RAW: {response.text}")

            try:
                parsed = clean_json(response.text)
                return parsed

            except Exception as e:
                logging.error(f"[Attempt {attempt}] Parse error: {e}")

    return {
        "is_job_related": False,
        "category": "not_job_related",
        "company": "unknown",
        "date": "unknown",
        "summary": "Failed to parse response",
        "confidence": 0.0,
        "language": "other"
    }

@traceable(name="analyze_email_safe")
def analyze_email_safe(email):
    raw = analyze_email(email["body"])
    raw["date"] = raw.get("date") or "unknown"
    raw["company"] = raw.get("company") or "unknown"
    raw["summary"] = raw.get("summary") or "unknown"

    raw["id"] = email["id"]

    return EmailAnalysis(**raw).dict()

@traceable(name="llm_call")
def call_llm(prompt: str, attempt: int):
    return model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.2
        }
    )