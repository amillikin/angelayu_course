import requests
import smtplib
from datetime import datetime, timezone
from dateutil import parser

FROM_EMAIL = "<email>"
APP_PASSWORD = "<password>"
TO_EMAIL = "<recipient>"
EMAIL_SUBJECT = "Subject:ISS Now Overhead!\n\n"
EMAIL_BODY = "Look up!"

MY_LAT = 41.487889
MY_LONG = -81.801783


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    return (
        (MY_LAT - 5 <= iss_latitude <= MY_LAT + 5) and
        (MY_LONG - 5 <= iss_longitude <= MY_LONG + 5)
    )


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json",
                            params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = parser.parse(data["results"]["sunrise"])
    sunset = parser.parse(data["results"]["sunset"])
    time_now = datetime.now(timezone.utc)

    # Ensuring we evaluate all possibilities of returned sunrise and sunset
    # Sunrise Today, Sunset Today, Current Time Today is after both
    # Sunrise is on the day following sunset, current time between both
    # Current Time is between midnight and Sunrise, Sunset value is after
    return (
        (sunrise < sunset <= time_now) or
        (sunset <= time_now <= sunrise) or
        (time_now <= sunrise < sunset)
    )


if is_iss_overhead() and is_night():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=FROM_EMAIL, password=APP_PASSWORD)
        connection.sendmail(
                            from_addr=FROM_EMAIL,
                            to_addrs=TO_EMAIL,
                            msg=f"{EMAIL_SUBJECT}{EMAIL_BODY}"
        )
