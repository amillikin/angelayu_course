from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

try:
    options = Options()
    #options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get("https://en.wikipedia.org/wiki/Main_Page")
    driver.find_element(By.NAME, "search").send_keys("Python", Keys.ENTER)
except Exception as error:
    print(f"{error}")
