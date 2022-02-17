import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

load_dotenv(os.environ.get("PYENV"))
TWITTER_E = os.getenv("TWITTER_EMAIL")
TWITTER_U = os.getenv("TWITTER_UN")
TWITTER_P = os.getenv("TWITTER_PASS")
TWITTER_URL = "https://twitter.com"
EXPECTED_DOWN = 100
EXPECTED_UP = 35
ISP_NAME = "<insert ISP>"
SPEEDTEST_URL = "https://www.speedtest.net/"

class InternetSpeedTwitterBot:


    def __init__(self):
        self.options = Options()
        self.driver = webdriver.Firefox(options=self.options)
        self.current_down = -1.0
        self.current_up = -1.0
        self.speed_test_url = ""


    def tweet(self):
        self.driver.get("https://twitter.com/i/flow/login")
        wait = WebDriverWait(self.driver, 30)

        # Enter Email
        login_field = wait.until(
            EC.visibility_of_element_located(
                (By.NAME, "text")
            )
        )
        login_field.send_keys(TWITTER_E)
        sleep(.5)
        login_field.send_keys(Keys.ENTER)
        sleep(.5)

        # Enter UN
        login_field = wait.until(
            EC.visibility_of_element_located(
                (By.NAME, "text")
            )
        )
        login_field.send_keys(TWITTER_U)
        sleep(.5)
        login_field.send_keys(Keys.ENTER)
        sleep(.5)

        # Enter PW
        pw_field = wait.until(
            EC.visibility_of_element_located(
                (By.NAME, "password")
            )
        )
        pw_field.send_keys(TWITTER_P)
        sleep(.5)
        pw_field.send_keys(Keys.ENTER)

        # Make tweet
        tweet_field = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.notranslate.public-DraftEditor-content")
            )
        )
        tweet_field.send_keys(
            f"""
            Expected speeds--D:{EXPECTED_DOWN}/U:{EXPECTED_UP}.\n
            Current speeds--D:{self.down}/U:{self.up} 😠\n
            Thanks {ISP_NAME}self.
            """
        )
        sleep(.3)
        tweet_field.send_keys(Keys.LEFT_CONTROL, Keys.ENTER)

    def get_current_speed(self):
        self.driver.get(SPEEDTEST_URL)
        self.driver.find_element(By.CLASS_NAME, "start-button").click()
        sleep(50)
        try_again = True
        time_out = 5
        while try_again:
            try:
                self.current_down = self.driver.find_element(By.CLASS_NAME, "download-speed").text
                self.current_up = self.driver.find_element(By.CLASS_NAME, "upload-speed").text
                try_again = False
            except NoSuchElementException as e:
                print(f"{e}")
                if time_out == 0:
                    try_again = False
                else:
                    time_out -= 1
                    sleep(10)
                continue
        self.speed_test_url = self.driver.current_url


bot = InternetSpeedTwitterBot()
bot.get_current_speed()
if (
    bot.current_down < EXPECTED_DOWN or 
    bot.current_up < EXPECTED_UP
):
    bot.tweet()
