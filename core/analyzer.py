import google.generativeai as genai
import os
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


@traceable(
    name="analyze_email_pipeline",
    metadata={"component": "email_classifier"}
)

def analyze_email(text: str):

    prompt = f"""
You are an expert email classifier for job applications.

Analyze the following email and return the requested structured data.

Email:
{text}
"""

    for attempt in range(2):
        with trace(
            name="retry_attempt",
            metadata={"attempt": attempt}
        ):
            try:
                response = call_llm(prompt, attempt)

                logging.info(f"[Attempt {attempt}] RAW: {response.text}")

                parsed = EmailAnalysis.model_validate_json(response.text)
                return parsed.model_dump()

            except Exception as e:
                logging.error(f"[Attempt {attempt}] Error: {e}")

    return {
        "is_job_related": False,
        "category": "not_job_related",
        "company": "unknown",
        "date": "unknown",
        "summary": "Failed to analyze email",
        "confidence": 0.0,
        "language": "other",
    }

@traceable(name="analyze_email_safe")
def analyze_email_safe(email):
    raw = analyze_email(email["body"])
    raw["id"] = email["id"]
    return EmailAnalysis(**raw).model_dump()

@traceable(name="llm_call")
def call_llm(prompt: str, attempt: int):
    return model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.2,
            "response_mime_type": "application/json",
            "response_schema": EmailAnalysis,
        },
    )