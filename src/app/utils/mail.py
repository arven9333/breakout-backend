from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from contextlib import contextmanager

from passlib.hash import bcrypt

from settings import EMAIL_PASSWORD, EMAIL, EMAIL_PORT


@contextmanager
def connect_to_email_server():
    port = EMAIL_PORT  # For SSL

    server = SMTP_SSL("smtp.gmail.com", port)
    server.login(EMAIL, EMAIL_PASSWORD)

    yield server

    server.quit()


def send_email(subject, message, recipient):
    msg = MIMEText(message, "html")
    msg['Subject'] = subject
    msg['From'] = EMAIL
    msg['To'] = recipient

    with connect_to_email_server() as server:
        server.send_message(msg)
    return True
