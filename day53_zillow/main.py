import os
import re
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import TypedDict
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv(os.environ.get("PYENV"))
ZILLOW_LINK = "https://www.zillow.com/homes/for_sale/house_type/3-_beds/2.0-_baths/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%2244107%22%2C%22mapBounds%22%3A%7B%22west%22%3A-82.33892679785369%2C%22east%22%3A-81.15240336035369%2C%22south%22%3A41.23403838925348%2C%22north%22%3A41.59039171622753%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22price%22%3A%7B%22min%22%3A175000%2C%22max%22%3A400000%7D%2C%22mp%22%3A%7B%22min%22%3A654%2C%22max%22%3A1495%7D%2C%22beds%22%3A%7B%22min%22%3A3%7D%2C%22baths%22%3A%7B%22min%22%3A2%7D%2C%22gar%22%3A%7B%22value%22%3Atrue%7D%2C%22basf%22%3A%7B%22value%22%3Atrue%7D%2C%22doz%22%3A%7B%22value%22%3A%2230%22%7D%7D%2C%22isListVisible%22%3Atrue%7D"


class HouseListing(TypedDict):
    address: str
    price: int
    beds: int
    bathrooms: int
    sqft: int
    link: str
    price_diff = int

class ZillowHouseHunter:


    def __init__(self):
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Firefox(options=self.options)
        self.listings = []
        self.excel_creds = Credentials.from_service_account_file(
            str(os.environ.get("EXCEL_SA_JSON")),
        )
        self.excel_sheet_id = os.getenv("EXCEL_SHEET_ID_53")
        self.excel_listing_sheet_range = "listings!A:G"
        self.excel_major_dimension = "ROWS"
        self.listing_data = []

    def scrape_houses(self):
        self.driver.get(ZILLOW_LINK)
        wait = WebDriverWait(
            driver=self.driver,
            timeout=30,
            ignored_exceptions=StaleElementReferenceException
        )

        total_listings = int(
            self.driver.find_element(
                By.CLASS_NAME,
                "total-text"
            ).text
        )
        page = 0
        while len(self.listings) < total_listings:
            page += 1

            if page > 1:
                self.driver.find_element(
                    By.XPATH,
                    f"//a[@title='Page {page}']"
                ).click()

            grid_h = wait.until(
                EC.presence_of_element_located(
                    (
                         By.XPATH,
                        "//ul[contains(@class,'photo-cards')]"
                    )
                )
            ).size['height']
            list_length = len(
                self.driver.find_elements(
                    By.TAG_NAME,
                    "article"
                )
            )
            scroll_y = grid_h / list_length

            for i in range(list_length):
                try:
                    link = wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "(//article"
                                "/div[contains(@class,'list-card-info')]"
                                "/a[contains(@class,'list-card-link')])"
                                f"[{i+1}]"
                            )
                        )
                    ).get_property("href")
                    address = wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "(//article"
                                "/div[contains(@class,'list-card-info')]"
                                "/a[contains(@class,'list-card-link')])"
                                f"[{i+1}]"
                            )
                        )
                    ).text
                    price_raw = wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "(//article"
                                "/div[contains(@class,'list-card-info')]"
                                "/div[contains(@class,'list-card-heading')]"
                                "/div[contains(@class,'list-card-price')])"
                                f"[{i+1}]"
                            )
                        )
                    ).text

                    price = int(
                        re.sub(
                            r"[^\d]*",
                            "",
                            price_raw
                        )
                    )

                    beds_raw = wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "(//article"
                                "/div[contains(@class,'list-card-info')]"
                                "/div[contains(@class,'list-card-heading')]"
                                "/ul[contains(@class,'list-card-details')]"
                                "/li[1])"
                                f"[{i+1}]"
                            )
                        )
                    ).text
                    beds = (
                        re.sub(
                            r"[^\d]*",
                            "",
                            beds_raw
                        )
                    )

                    bathrooms_raw = wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "(//article"
                                "/div[contains(@class,'list-card-info')]"
                                "/div[contains(@class,'list-card-heading')]"
                                "/ul[contains(@class,'list-card-details')]"
                                "/li[2])"
                                f"[{i+1}]"
                            )
                        )
                    ).text
                    bathrooms = (
                        re.sub(
                            r"[^\d]*",
                            "",
                            bathrooms_raw
                        )
                    )
                    sqft_raw = wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "(//article"
                                "/div[contains(@class,'list-card-info')]"
                                "/div[contains(@class,'list-card-heading')]"
                                "/ul[contains(@class,'list-card-details')]"
                                "/li[3])"
                                f"[{i+1}]"
                            )
                        )
                    ).text
                    sqft = (
                        re.sub(
                            r"[^\d]*",
                            "",
                            sqft_raw
                        )
                    )

                    listing: HouseListing = {
                        "address": address,
                        "price": price,
                        "beds": beds,
                        "bathrooms": bathrooms,
                        "sqft": sqft,
                        "link": link,
                        "price_diff": 0
                    }
                    self.listings.append(listing)
                    
                    self.driver.execute_script(
                        f"document.getElementById('search-page-list-container').scrollBy(0,{scroll_y})"
                    )
                except NoSuchElementException as e:
                    print(f"{e}")    
                continue

    def read_spreadsheet(self):
        try:
            service = build('sheets', 'v4', credentials=self.excel_creds)

            sheet = service.spreadsheets()
            
            result = sheet.values().get(
                spreadsheetId=self.excel_sheet_id,
                range=self.excel_listing_sheet_range,
                majorDimension=self.excel_major_dimension,
            ).execute()
            self.listing_data = result.get('values', [])
        except HttpError as err:
            print(err)

    def update_spreadsheet(self, update_data):
        try:
            service = build('sheets', 'v4', credentials=self.excel_creds)

            body = {
                "majorDimension": self.excel_major_dimension,
                "values": update_data
            }
            result = service.spreadsheets().values().update(
                spreadsheetId=self.excel_sheet_id,
                valueInputOption="RAW",
                range=self.excel_listing_sheet_range,
                body=body
            ).execute()
        except HttpError as err:
            print(err)


bot = ZillowHouseHunter()
bot.scrape_houses()
bot.read_spreadsheet()
data = bot.listing_data
past_addresses = [row[0] for row in data[1:]]

# Let's look for and remove old data items.
# We'll pop them out so we don't get duplicates,
# but we'll keep record of any price changes for our benefit.
if len(past_addresses) > 0:
    for i in range(len(bot.listings)):
        if bot.listings[i]["address"] in past_addresses:
            old_index = past_addresses.index(bot.listings[i]["address"]) + 1
            if data[old_index][1] != bot.listings[i]["price"]:
                diff = bot.listings[i]["price"] - data[old_index][1]
                bot.listings[i]["price_diff"] = diff
            data.pop(old_index)

# Now that we've consolidated our changes
# Let's combine data sets for updated the spreadsheet
# While it may have saved effort to start listings as a list of lists
# I prefer starting with a dictionary for readability, so let's convert it now.
new_data = [
    [
        listing["address"],
        listing["price"],
        listing["beds"],
        listing["bathrooms"],
        listing["sqft"],
        listing["link"],
        listing["price_diff"],
    ]
    for listing in bot.listings
]
data.extend(new_data)
bot.update_spreadsheet(data)
