"""
Script for setting up email so that any suggestions or feedbacks will be sent to admin
"""

import os
import ssl
import yaml
import smtplib
from datetime import datetime


with open("config.yaml") as config_file:
    config_keys = yaml.load(config_file, Loader=yaml.Loader)


def send_email_to_self(name, email, feedback):
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = config_keys["GMAIL_SENDER_EMAIL"]
    password = config_keys["GMAIL_SENDER_PASSWORD"]
    receiver_email = os.environ.get("EMAIL_RECEIVER") or "Enter receiver address"
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
