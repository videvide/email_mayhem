from collections import deque
import pdb
from urllib.parse import urlsplit
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

original_url = "https://www.lansfast.se/maklare/vastra-gotaland/ale/"
# original_url = (
#     "https://www.lansfast.se/maklare/vastra-gotaland/ale/medarbetare/lasse-knaving/"
# )
deep_link_contains = "medarbetare/"

unscraped = deque([original_url])
scraped = set()

emails = set()


options = Options()
options.add_argument("headless")
# options.headless = True <- fungerar med!

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

while len(unscraped):
    url = unscraped.popleft()
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

    # pdb.set_trace()
    email_elements = soup.find_all(
        "span", string=lambda string: string and "@lansfast.se" in string
    )
    for email_element in email_elements:
        print(email_element.text)
        emails.add(email_element.text)

    # pdb.set_trace()
    anchors = soup.find_all("a", href=lambda href: href and deep_link_contains in href)
    for anchor in anchors:
        link = original_url + anchor.attrs["href"]
        print(link)

        if not link.endswith(".gz"):
            if not link in unscraped and not link in scraped:
                unscraped.append(link)

print(emails)
driver.quit()
