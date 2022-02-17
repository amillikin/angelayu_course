from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

try:
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get("https://en.wikipedia.org/wiki/Main_Page")
    article_count = driver.find_element(
        by=By.CSS_SELECTOR,
        value="#articlecount a"
    )
    print(f"{article_count.text}")
except Exception as error:
    print(f"{error}")
