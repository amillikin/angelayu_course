import smtplib
import requests
import os
from dotenv import load_dotenv

load_dotenv(os.environ.get("PYENV"))

FROM_EMAIL = os.getenv("APP_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
TO_EMAIL = os.getenv("APP_RECIPIENT")
EMAIL_SUBJECT = "Subject:It's gon rain!\n\n"
EMAIL_BODY = "Bring an umbrella today!"

OW_API_KEY = os.getenv("OWM_API_KEY")
MY_LAT = os.getenv("LAT") 
MY_LONG = os.getenv("LONG")
EXCLUDES = "current,minutely,daily"
OW_API_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"

API_PARAMS = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": OW_API_KEY,
    "exclude": EXCLUDES
}

response = requests.get(url=OW_API_ENDPOINT, params=API_PARAMS)
response.raise_for_status()
data = response.json()
will_rain = False

for data_hour in data["hourly"][:12]:
    for weather_item in data_hour["weather"]:
        if weather_item["id"]:
            will_rain = True

if will_rain:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=FROM_EMAIL, password=APP_PASSWORD)
        connection.sendmail(
                            from_addr=FROM_EMAIL,
                            to_addrs=TO_EMAIL,
                            msg=f"{EMAIL_SUBJECT}{EMAIL_BODY}"
        )
