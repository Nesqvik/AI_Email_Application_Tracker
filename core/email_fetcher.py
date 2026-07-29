import imaplib
import email

def fetch_emails(user_email, password):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(user_email, password)

    mail.select("inbox")
    status, messages = mail.search(None, "ALL")

    email_list = []

    for num in messages[0].split()[-10:]:
        status, msg_data = mail.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        subject = msg["subject"]
        from_ = msg["from"]

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        email_list.append({
            "subject": subject,
            "from": from_,
            "body": body
        })

    return email_list