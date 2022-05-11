# https://medium.com/swlh/how-to-scrape-email-addresses-from-a-website-and-export-to-a-csv-file-c5d1becbd1a0

import pandas as pd
from urllib.parse import urlsplit
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

start_url = input("Ange URL: ")
deep_link = input("Ange hela eller del av vidarelänk: ")
csv_name = input("Ange CSV namn: ")


options = Options()
options.headless = True
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)


def save_emails(emails):
    df = pd.DataFrame(emails, columns=["email"])
    df.to_csv(csv_name + ".csv", index=False)
    print("--------------------------------------")
    print(f"Amount of emails saved: {len(emails)}")


def scrape_emails(links):
    office_links = set()
    office_links.update(links)
    scraped = set()
    emails = set()

    while len(office_links):
        url = office_links.pop()
        scraped.add(url)

        driver.get(url)

        soup = BeautifulSoup(driver.page_source, "lxml")

        elements = soup.find_all("a", href=lambda href: href and "mailto:" in href)
        for element in elements:
            emails.add(element.attrs["href"])
            print(f"Email saved: \n{element.attrs['href']}")

        scraped.add(url)

    save_emails(emails)


def get_office_links(start_url):
    url = start_url
    office_links = set()

    parts = urlsplit(url)

    base_url = "{0.scheme}://{0.netloc}".format(parts)

    if "/" in parts.path:
        path = url[: url.rfind("/") + 1]
    else:
        path = url

    print("Crawling URL %s" % url)

    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "lxml")

    anchors = soup.find_all("a", href=lambda href: href and deep_link in href)
    for anchor in anchors:
        if "href" in anchor.attrs:
            link = anchor.attrs["href"]
        else:
            link = ""

        # resolve relative links (starting with /)
        if link.startswith("/"):
            link = base_url + link

        elif not link.startswith("http"):
            link = path + link

        office_links.add(link)
        print(f"Saved Link: \n{link}")

    scrape_emails(office_links)


get_office_links(start_url)
