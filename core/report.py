from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
import mimetypes
import os

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)

from core.storage import get_all_job_emails
from config.settings import load_settings


SCOPES = [
    "https://www.googleapis.com/auth/gmail.send"
]

BASE_DIR = Path(__file__).resolve().parents[1]
REPORT_DIR = BASE_DIR / "data" / "reports"

TOKEN_PATH = BASE_DIR / "token.json"


def generate_pdf(emails):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    month = datetime.now().strftime("%B_%Y")
    pdf_path = REPORT_DIR / f"job_report_{month}.pdf"

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=landscape(A4),
        rightMargin=10 * mm,
        leftMargin=10 * mm,
        topMargin=10 * mm,
        bottomMargin=10 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]

    cell_style = ParagraphStyle(
        "CellStyle",
        parent=styles["Normal"],
        fontSize=8,
        leading=10,
    )

    elements = []

    title = f"Monthly Job Application Report — {datetime.now().strftime('%B %Y')}"

    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 10))

    total = len(emails)

    categories = {}

    for email in emails:
        category = email.category
        categories[category] = categories.get(category, 0) + 1

    elements.append(
        Paragraph(
            f"<b>Total job-related emails:</b> {total}",
            styles["Normal"],
        )
    )

    elements.append(Spacer(1, 10))

    table_data = [
        [
            Paragraph("<b>Company</b>", cell_style),
            Paragraph("<b>Category</b>", cell_style),
            Paragraph("<b>Date</b>", cell_style),
            Paragraph("<b>Summary</b>", cell_style),
            Paragraph("<b>Language</b>", cell_style),
            Paragraph("<b>Confidence</b>", cell_style),
        ]
    ]

    for email in emails:
        table_data.append(
            [
                Paragraph(str(email.company or ""), cell_style),
                Paragraph(str(email.category or ""), cell_style),
                Paragraph(str(email.date or ""), cell_style),
                Paragraph(str(email.summary or ""), cell_style),
                Paragraph(str(email.language or ""), cell_style),
                Paragraph(
                    f"{email.confidence:.0%}"
                    if email.confidence is not None
                    else "",
                    cell_style,
                ),
            ]
        )

    if len(table_data) == 1:
        table_data.append(
            [
                Paragraph("No job-related emails found.", cell_style),
                "",
                "",
                "",
                "",
                "",
            ]
        )

    table = Table(
        table_data,
        colWidths=[
            35 * mm,
            35 * mm,
            25 * mm,
            100 * mm,
            25 * mm,
            25 * mm,
        ],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5E7EB")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    elements.append(table)

    doc.build(elements)

    return pdf_path


def send_email(pdf_path, recipient_email):
    if not TOKEN_PATH.exists():
        raise FileNotFoundError(
            "token.json not found. Connect Gmail first."
        )

    credentials = Credentials.from_authorized_user_file(
        TOKEN_PATH,
        SCOPES,
    )

    gmail = build(
        "gmail",
        "v1",
        credentials=credentials,
    )

    message = EmailMessage()

    message["To"] = recipient_email
    message["Subject"] = (
        f"Monthly Job Application Report — "
        f"{datetime.now().strftime('%B %Y')}"
    )
    message["From"] = "me"

    message.set_content(
        "Hello,\n\n"
        "Please find attached your monthly job application report.\n\n"
        "This report was generated automatically by "
        "AI Email Application Tracker.\n"
    )

    pdf_data = pdf_path.read_bytes()

    message.add_attachment(
        pdf_data,
        maintype="application",
        subtype="pdf",
        filename=pdf_path.name,
    )

    encoded_message = message.as_bytes()

    import base64

    raw_message = base64.urlsafe_b64encode(
        encoded_message
    ).decode()

    gmail.users().messages().send(
        userId="me",
        body={"raw": raw_message},
    ).execute()


def send_report():
    settings = load_settings()

    if not settings.get("monthly_report"):
        print("Monthly report is disabled.")
        return

    recipient_email = settings.get("email")

    if not recipient_email:
        print("Recipient email is not configured.")
        return

    emails = get_all_job_emails()

    if not emails:
        print("No job-related emails found.")
        return

    pdf_path = generate_pdf(emails)

    send_email(
        pdf_path,
        recipient_email,
    )

    print(f"Report sent to {recipient_email}")
    print(f"PDF saved to {pdf_path}")