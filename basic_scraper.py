import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

print("Basic Scraper")
print("-------------")
url = input("Ange URL: ")
csv_name = input("Ange CSV namn: ")
emails = set()

options = Options()
options.headless = True

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

print("Crawling URL %s" % url)

driver.get(url)

soup = BeautifulSoup(driver.page_source, "lxml")

elements = soup.find_all("a", href=lambda href: href and "mailto:" in href)
for element in elements:
    emails.add(element.attrs["href"])
    print(f"Email saved: \n{element.attrs['href']}")

print("--------------------------------------")
print(f"Amount of emails saved: {len(emails)}")
driver.quit()

df = pd.DataFrame(emails, columns=["email"])
df.to_csv(csv_name + ".csv", index=False)
