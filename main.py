from fastapi import FastAPI
from core.storage import get_all_job_emails

app = FastAPI()

@app.get("/emails")
def get_emails():
    data = get_all_job_emails()
    return [e.__dict__ for e in data]