import os
import smtplib
from email.message import EmailMessage


def send_html_email(subject: str, html_path: str, text_path: str | None = None):
    smtp_host = os.environ["SMTP_HOST"]
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ["SMTP_USER"]
    smtp_pass = os.environ["SMTP_PASS"]
    mail_from = os.environ.get("EMAIL_FROM", smtp_user)
    mail_to = os.environ["EMAIL_TO"]

    ehlo_name = os.environ.get("SMTP_EHLO_NAME", "westlake.edu.cn")
    timeout = int(os.environ.get("SMTP_TIMEOUT", "20"))

    with open(html_path, "r", encoding="utf-8") as f:
        html_body = f.read()

    if text_path and os.path.exists(text_path):
        with open(text_path, "r", encoding="utf-8") as f:
            text_body = f.read()
    else:
        text_body = "Papers Daily (HTML version)."

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = mail_from
    msg["To"] = mail_to
    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP(smtp_host, smtp_port, timeout=timeout, local_hostname=ehlo_name) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)