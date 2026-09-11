# AI Email Application Tracker


An AI-powered application that automatically analyzes recruitment emails from a connected Gmail account.

The system identifies job-related emails, classifies them into recruitment stages such as interview invitations, offers, assessments and rejections, and presents the results in an interactive dashboard.

Users can search, filter and export the analyzed emails as a PDF report.

## Overview

Managing recruitment emails can quickly become overwhelming during a job search.

Important interview invitations or offers are often mixed with newsletters, promotions and other personal emails.

This application automatically analyzes Gmail messages using AI and extracts only recruitment-related communication.

The application allows users to:

- Connect a Gmail account securely using Google OAuth
- Analyze recent emails with an LLM
- Detect recruitment-related messages
- Classify emails into hiring stages
- View results inside a dashboard
- Search by company
- Filter by recruitment category
- Export analyzed emails as a PDF report

<table>
  <tr>
    <td align="center">
      <b>Start Screen</b><br/>
      <img src="images/img_start.png" alt="Start Screen" width="650"/>
    </td>
  </tr>
</table>

## Features

- Gmail OAuth authentication
- Automatic retrieval of recent Gmail messages
- AI-powered recruitment email analysis
- Detection of job-related emails only
- Classification into:
  - Interview Invitation
  - Interview Follow-up
  - Assessment
  - Offer
  - Rejection
  - Application Received
  - Networking
- Company extraction
- Email summary generation
- Search by company
- Category filtering
- Dashboard statistics
- PDF export
- Responsive Streamlit interface

## Email Analysis

The application connects to Gmail and retrieves the latest emails.

Each email is processed by an LLM that determines:

- whether the email is recruitment related
- recruitment stage
- company name
- detected language
- date
- concise summary

Only recruitment-related emails are displayed in the dashboard.

## Dashboard

The dashboard provides:

- Total recruitment emails
- Interview count
- Offer count
- Rejection count

Users can additionally:

- Search companies
- Filter recruitment stages
- View detailed email cards
- Export results to PDF

### Background Agent

The project also includes a background worker.

The worker periodically:

1. Connects to Gmail
2. Fetches new emails
3. Runs AI analysis
4. Detects new recruitment emails
5. Updates stored results

This enables continuous monitoring without manually checking the inbox.

### PDF Export

Users can export all filtered recruitment emails into a structured PDF report.

Each entry contains:

- Company
- Category
- Date
- Summary
- Language

### System Workflow

1. User connects Gmail
2. Google OAuth authentication
3. Latest emails are downloaded
4. Gemini analyzes every email
5. Job-related emails are extracted
6. Dashboard displays results
7. User searches or filters emails
8. Results can be exported as PDF
        
### Technologies

- Python
- Streamlit
- Google Gmail API
- Google OAuth 2.0
- Google Gemini API
- Pandas
- ReportLab

## Limitations

- Only the latest emails are analyzed.
- Email classification depends on LLM reasoning.
- Incorrect summaries or classifications may occasionally occur.
- Recruitment emails written in uncommon formats may not be detected correctly.

## Privacy

- Gmail access is read-only.
- Emails are processed only for analysis.
- OAuth credentials remain on the user's machine.
- The application does not intentionally store email content permanently

### Ethics & Safety

This application is intended to assist users during the recruitment process.
AI-generated classifications should be reviewed by the user before making important decisions.

## Installation
- Run `uv sync`

## How to run

- Run `uv run streamlit run ./email_check_app.py`

## Gmail authentication

Each user must configure their own Google OAuth credentials.

1. Enable the Gmail API in Google Cloud.
2. Create OAuth 2.0 credentials.
3. Download the credentials file.
4. Place it in the project as:

```text
credentials/client_secret.json
```

## Docker

The application can also be run using Docker.

### Build the Docker image
```bash
docker build -t email-tracker
```
### Run the container
```bash
docker run --env-file .env -p 8501:8501 email-tracker
```

The application will be available at:

http://localhost:8501


### Docker Compose

If Docker Compose is installed, the application can be started with:
```bash
docker compose up --build
```

If the older standalone Docker Compose command is installed, use:
```bash
docker-compose up --build
```

The application will be available at:

http://localhost:8501

To stop the application:
```bash
docker compose down
```

## Application Preview

</table>
    <td align="center">
      <b>Food Analysis & Results</b><br/>
      <img src="images/img_res.png" alt="Input Example Screen" width="850"/>
    </td>
  </tr>
</table>

