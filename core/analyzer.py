from openai import OpenAI
client = OpenAI()

def analyze_email(text):
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": """
You are an expert email classifier for job applications.

Your task is to analyze emails and extract structured information.

Rules:
- Be precise and factual
- Do not hallucinate
- If information is missing, return "unknown"
- Always return valid JSON
"""
            },
            {
                "role": "user",
                "content": f"""
Analyze the following email and extract structured data.

Return JSON with this exact schema:
{{
  "is_job_related": boolean,
  "category": "interview" | "rejection" | "other",
  "company": string,
  "date": string,
  "summary": string
}}

Definitions:
- "interview" → invitation to interview, next steps, scheduling
- "rejection" → decline, not selected, position filled
- "other" → job-related but unclear or neutral

Instructions:
- Extract the company name from signature or sender
- Extract the date mentioned in the email (not metadata)
- Keep summary short (1–2 sentences)
- If not job-related → set category = "other"

Email:
{text}
"""
            }
        ],
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content