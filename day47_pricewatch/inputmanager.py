import re
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from sqlmanager import SQLManager

EMAIL_REGEX = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
AMAZON_URL = "https://www.amazon.com/dp/"

class InputManager:


    def __init__(self):
        self.user_email = ""
        self.get_user_email()
        self.db = SQLManager(
            db_file_path="./data/price_history.db",
            user_email=self.user_email
        )
        self.html = "" 
        self.page_id = ""
        self.price_data = ()
        self.threshold = 0.0

        self.get_html_data()
        if self.html is not None:
            self.get_price_data()
            self.get_threshold()
            self.insert_new_watch()


    def get_user_email(self):
        while not re.match(EMAIL_REGEX, self.user_email):
            self.user_email = input("Please input your email address: ").lower().strip()

    def get_html_data(self):
        while self.html == "":
            self.page_id = input("Please input an Amazon page ID e.g. B0015SBILG\n> ")
            self.html = self.get_html()
            if self.html is None:
                print(f"{self.page_id} does not appear to be a valid ID.")


    def get_html(self):
        try:
            options = Options()
            options.headless = True
            driver = webdriver.Firefox(options=options)
            driver.get(AMAZON_URL + self.page_id)
            sleep(1)
            return driver.page_source
        except Exception as error:
            print(f"{error}")
            return None


    def get_price_data(self):
        site_data = BeautifulSoup(self.html, 'html.parser')

        price_whole = site_data.select_one(".a-price-whole").get_text()
        price_decimal = site_data.select_one(".a-price-fraction").get_text()
        product_title = site_data.select_one("#productTitle").get_text()

        price = float(price_whole) + float(price_decimal)/100
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = (
            price,
            now, 
            price,
            now,
            price,
            now,
            product_title.strip()
        )
        self.price_data = data


    def get_threshold(self):
        while self.threshold == 0.0:
            response = input(
                f"Data found for:\n{self.price_data[6]}\n" +
                "At what price would you like to receive a notification?\n" +
                f"Current Price: {self.price_data[0]}\n" +
                "> $"
            )
            try:
                self.threshold = float(response)
            except:
                print(f"{response} is not a valid threshold (e.g. 10.00)")
                self.threshold = 0


    def insert_new_watch(self):
        new_price_watch = (
            self.page_id,
            self.price_data[0],
            self.price_data[1],
            self.price_data[2],
            self.price_data[3],
            self.price_data[4],
            self.price_data[5],
            self.price_data[6],
            self.threshold,
            self.db.user_id
        )

        self.db.add_price_watch(new_price_watch)
