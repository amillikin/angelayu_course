from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from datetime import datetime
from datetime import timedelta

COOKIE_URL = "https://orteil.dashnet.org/cookieclicker/"

class CookieTime:


    def __init__(self):
        try:
            self.options = Options()
            self.driver = webdriver.Firefox(options=self.options)
            self.driver.get(COOKIE_URL)
            self.last_check = datetime.now()
            self.next_check = self.last_check + timedelta(seconds=5)
            self.cookie_clicker()
        except Exception as error:
            print(f"{error}")


    def cookie_clicker(self):
        while self.last_check < self.next_check:
            self.driver.find_element(By.ID, "bigCookie").click()
        self.buy_stuff()
        self.reset_time()
        #self.cookie_clicker()


    def buy_stuff(self):
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".enabled")
        if len(elements) > 0:
            elements[-1].click()


    def reset_time(self):
        self.last_check = datetime.now()
        self.next_check = self.last_check + timedelta(seconds=5)


cc = CookieTime()

