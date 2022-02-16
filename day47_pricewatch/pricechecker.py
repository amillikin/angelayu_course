from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from sqlmanager import SQLManager
from emailmanager import EmailManager

AMAZON_URL = "https://smile.amazon.com/dp/"


class PriceChecker:


    def __init__(self):
        self.db = SQLManager(
            db_file_path="./data/price_history.db",
        )
        self.pages = self.db.get_all_pages()
        self.new_prices = {}
        self.notify_list = []
        if len(self.pages) > 0:
            self.get_current_prices()
            self.notify_list = self.db.get_notify_list(self.new_prices)
            if len(self.notify_list) > 0:
               self.generate_notifications() 
        else:
            print("No price watch items found in database.")


    def get_current_prices(self):
        for page in self.pages:
            html = self.get_html(page[0])
            current_price = self.get_price_data(html)
            self.new_prices[page[0]] = current_price

    def get_html(self, page_id: str):
        try:
            options = Options()
            options.headless = True
            driver = webdriver.Firefox(options=options)
            driver.get(AMAZON_URL + page_id)
            sleep(1)
            return driver.page_source
        except Exception as error:
            print(f"{error}")


    def get_price_data(self, html: str):
        site_data = BeautifulSoup(html, 'html.parser')

        price_whole = site_data.select_one(".a-price-whole").get_text()
        price_decimal = site_data.select_one(".a-price-fraction").get_text()

        price = float(price_whole) + float(price_decimal)/100

        return price


    def generate_notifications(self):
        notifier = EmailManager()
        for item in self.notify_list:
            subject = "Subject:New Price Alert!\n\n"
            body = f"""
            Price Alert for item {item[1]}!\n
            Your threshold price for this item: ${item[3]}\n
            Current price for this item: ${item[2]}\n
            Buy this item now at {AMAZON_URL}{item[0]}
            """
            notifier.send_email(
                email_subject=subject,
                email_body=body,
                recipient=item[4]
            )
