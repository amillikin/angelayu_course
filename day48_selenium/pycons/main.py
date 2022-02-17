from selenium import webdriver
from selenium.webdriver.firefox.options import Options

try:
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get("https://www.python.org/")
    event_times = driver.find_elements_by_css_selector(".event-widget time")
    event_names = driver.find_elements_by_css_selector(".event-widget li a")
    events = {}
    for i in range(len(event_names)):
        events[i] = {
            "date": event_times[i].text,
            "name": event_names[i].text
        }
    print(f"{events}")
except Exception as error:
    print(f"{error}")
