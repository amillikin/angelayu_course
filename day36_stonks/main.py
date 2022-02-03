import smtplib
import requests
import os
from dotenv import load_dotenv

load_dotenv(os.environ.get("PYENV"))

FROM_EMAIL = os.getenv("APP_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
TO_EMAIL = os.getenv("APP_RECIPIENT")

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
AV_STONKS_KEY = os.getenv("AV_STONKS_KEY")

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla"

STONKS_PARAMS  = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": AV_STONKS_KEY,
}

NEWS_PARAMS = {
    "apikey": NEWSAPI_KEY,
    "qInTitle": COMPANY_NAME,
}

stonk_response = requests.get(url=STOCK_ENDPOINT, params=STONKS_PARAMS)
stonk_response.raise_for_status()
stonks_data = stonk_response.json()["Time Series (Daily)"]
stonks_data_list = [day_data for (key, day_data) in stonks_data.items()]
stonk_close_1d_ago = float(stonks_data_list[0]["4. close"])
stonk_close_2d_ago = float(stonks_data_list[1]["4. close"])

stonk_diff = stonk_close_1d_ago - stonk_close_2d_ago
if stonk_diff < 0:
    stonks_direction = "↓"
else:
    stonks_direction = "↑"
stonk_diff_perc = round((abs(stonk_diff) / stonk_close_1d_ago) * 100)

if stonk_diff_perc > 1:
    news_response = requests.get(url=NEWS_ENDPOINT, params=NEWS_PARAMS)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    num_articles = len(news_data)
    if num_articles >= 3:
        top_articles = news_data[:3]
        is_news = True
    elif num_articles > 0:
        is_news = True
    else:
        is_news = False

    if is_news:
        email_subject = (
            f"Subject:{COMPANY_NAME}'s stonks are {stonks_direction}" + 
            f"{stonk_diff_perc}% - Top News Inside\n\n"
        )
        email_body = ""

        for article in top_articles:
            email_body += (
                f"Headline: {article['title']}\n" +
                f"Brief: {article['description']}\n\n"
            )

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=FROM_EMAIL, password=APP_PASSWORD)
            connection.sendmail(
                from_addr=FROM_EMAIL,
                to_addrs=TO_EMAIL,
                msg=(f"{email_subject}{email_body}").encode("utf8"),
            )
