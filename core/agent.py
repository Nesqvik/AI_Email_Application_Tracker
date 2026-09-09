from core.email_fetcher import fetch_emails
from core.analyzer import analyze_email_safe
from core.storage import save_email


def run_agent():
    emails = fetch_emails()

    for email in emails:
        try:
            result = analyze_email_safe(email)

            print("📩 EMAIL RESULT:")
            print(result)

             # FILTER ONLY JOB RELATED
            if result["is_job_related"]:
                save_email(result)

        except Exception as e:
            print("Agent error:", e)