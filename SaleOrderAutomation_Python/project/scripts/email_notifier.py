# project/scripts/email_notifier.py

import smtplib
from email.message import EmailMessage
from pathlib import Path
from config.config import *

def send_execution_mail(subject, body, attachments):
    msg = EmailMessage()
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(RECIPIENTS)
    msg["Subject"] = subject
    msg.set_content(body)

    for file in attachments:
        file_path = Path(file)

        if not file_path.exists():
            raise FileNotFoundError(f"Attachment not found: {file_path}")

        with open(file_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="octet-stream",
                filename=file_path.name
            )

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

    print("📧 Email sent successfully")
