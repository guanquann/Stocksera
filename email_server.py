import os
import ssl
import smtplib
from datetime import datetime


def send_email(name, email, feedback):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = os.environ.get("EMAIL_SENDER") or "Enter your address"
    receiver_email = os.environ.get("EMAIL_RECEIVER") or "Enter receiver address"
    password = os.environ.get("EMAIL_PW") or "Enter your password"
    message = f"""\
Subject: Feedback!

This message is sent from Stocksera Admin.

Name: {name}
Email: {email}
Feedback: {feedback}

Time Sent: {str(datetime.utcnow()).split(".")[0]} UTC

Thank you & have a nice day!
"""
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
