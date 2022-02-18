# 
# NOTE Twitter has follow limitations. Typically, 400/day
# and up to 5,000 until you have people following you back.
# REF: https://help.twitter.com/en/using-twitter/twitter-follow-limit
#
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

class TwitterFollowerBot:


    def __init__(self):
        self.options = Options()
        self.driver = webdriver.Firefox(options=self.options)
        self.login()

    def login(self):
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
        sleep(4)


    def follow_followers(self, account):
        self.driver.get(f"https://twitter.com/{account}/followers")
        wait = WebDriverWait(self.driver, 30)
        sleep(4)
        new_height = self.driver.execute_script(
            "return document.body.scrollHeight"
        )
        last_height = -1 
        button = self.driver.find_element(
            By.XPATH, 
            "//div[starts-with(@aria-label, 'Follow @')]"
        )
        button.click()
        print(f"Following... {button.get_attribute('aria-label')}")
        continue_scrolling = True
        while continue_scrolling: 
            try: 
                button = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH, 
                            "//div[starts-with(@aria-label, 'Follow @')]"
                        )
                    )
                )
                button.click()
                print(f"Following... {button.get_attribute('aria-label')}")
            except (
                ElementNotInteractableException,
                ElementClickInterceptedException,
            ) as e:
                print(f"{e}")
                self.driver.execute_script("arguments[0].scrollIntoView()", button)
                last_height = new_height
                new_height = self.driver.execute_script(
                    "return document.body.scrollHeight;"
                )
                if new_height == last_height:
                    continue_scrolling = False
                continue
            except StaleElementReferenceException as e:
                # This tends to pop up when an attempted follow
                # has to approve your follow. I hit follow limitations
                # before I was able to fully debug this issue.
                print(f"{e}")
                sleep(2)
                self.driver.execute_script("arguments[0].scrollIntoView()", button)
                last_height = new_height
                new_height = self.driver.execute_script(
                    "return document.body.scrollHeight;"
                )
                if new_height == last_height:
                    continue_scrolling = False
                continue


bot = TwitterFollowerBot()
bot.follow_followers("SwiftOnSecurity")
