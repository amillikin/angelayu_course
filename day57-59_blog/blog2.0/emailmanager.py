import os
import smtplib
from dotenv import load_dotenv

class EmailManager:


    def __init__(self):
        load_dotenv(os.environ.get("PYENV"))
        self.FROM_EMAIL = os.getenv("APP_EMAIL")
        self.APP_PASSWORD = os.getenv("APP_PASSWORD")


    def send_email(self, email_subject, email_body, recipient):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=self.FROM_EMAIL, password=self.APP_PASSWORD)
            connection.sendmail(
                from_addr=self.FROM_EMAIL,
                to_addrs=recipient,
                msg=(f"{email_subject}{email_body}").encode("utf8"),
            )
