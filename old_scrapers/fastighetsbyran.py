# https://medium.com/swlh/how-to-scrape-email-addresses-from-a-website-and-export-to-a-csv-file-c5d1becbd1a0
import os
import sys
import pandas as pd
from urllib.parse import urlsplit
from collections import deque
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

csv_name = "fastighetsbyran"
email_ending = "se"

unscraped = set()
scraped = set()
emails = set()

with open(os.path.join(sys.path[0], "fb_links.txt"), "r") as file:
    for line in file:
        unscraped.add(line.strip())

print(unscraped)

options = Options()
options.headless = True
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

while len(unscraped):
    url = unscraped.pop()
    scraped.add(url)

    parts = urlsplit(url)

    base_url = "{0.scheme}://{0.netloc}".format(parts)

    # magi:
    if "/" in parts.path:
        path = url[: url.rfind("/") + 1]
    else:
        path = url

    print("Crawling URL %s" % url)

    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "lxml")

    new_emails = set()
    email_elements = soup.find_all("a", href=lambda href: href and "mailto" in href)
    if email_elements:
        for element in email_elements:
            new_emails.add(element["href"]) if not None else None

    print(new_emails)
    emails.update(new_emails)

df = pd.DataFrame(emails, columns=["email"])
df.to_csv(csv_name + ".csv", index=False)

driver.quit()
