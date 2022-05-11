import pandas as pd
from urllib.parse import urlsplit
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

url = "https://www.magnussonmakleri.se/kontakt/alla/"
emails = set()
csv_name = "magnusson"

options = Options()
options.add_argument("headless")
# options.headless = True <- fungerar med!

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

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

elements = soup.find_all("a", href=lambda href: href and "mailto:" in href)
for element in elements:
    print(element.attrs["href"])
    emails.add(element.attrs["href"])

df = pd.DataFrame(emails, columns=["email"])
df.to_csv(csv_name + ".csv", index=False)

print(emails)
driver.quit()
