import os
import requests
import smtplib
from dotenv import load_dotenv

class NotificationManager:
    load_dotenv(os.environ.get("PYENV"))
    FROM_EMAIL = os.getenv("APP_EMAIL")
    APP_PASSWORD = os.getenv("APP_PASSWORD")
    TO_EMAIL = os.getenv("APP_RECIPIENT")


    def __init__(self, email_subject: str, email_body):
        self.subject = email_subject
        self.body = email_body


    def send_email(self):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=self.FROM_EMAIL, password=self.APP_PASSWORD)
            connection.sendmail(
                from_addr=self.FROM_EMAIL,
                to_addrs=self.TO_EMAIL,
                msg=(f"{self.subject}{self.body}").encode("utf8"),
            )
