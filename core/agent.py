
def agent_pipeline():
    emails = fetch_emails()

    results = []
    for e in emails:
        analysis = analyze_email(e["body"])
        results.append(analysis)

    return results