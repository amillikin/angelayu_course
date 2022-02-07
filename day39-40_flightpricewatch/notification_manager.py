import os
import requests
import smtplib
from dotenv import load_dotenv

class NotificationManager:


    def __init__(self):
        load_dotenv(os.environ.get("PYENV"))
        self.FROM_EMAIL = os.getenv("APP_EMAIL")
        self.APP_PASSWORD = os.getenv("APP_PASSWORD")
        self.TO_EMAIL = os.getenv("APP_RECIPIENT")


    def send_email(self, email_subject, email_body):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=self.FROM_EMAIL, password=self.APP_PASSWORD)
            connection.sendmail(
                from_addr=self.FROM_EMAIL,
                to_addrs=self.TO_EMAIL,
                msg=(f"{email_subject}{email_body}").encode("utf8"),
            )
