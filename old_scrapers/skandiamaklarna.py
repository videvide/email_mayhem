# https://medium.com/swlh/how-to-scrape-email-addresses-from-a-website-and-export-to-a-csv-file-c5d1becbd1a0

import requests
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd

original_url = "https://www.skandiamaklarna.se/kontor/vara-maklare"
deep_link_starts_with = "/personal/"
deep_link_ends_with = ""
csv_name = "skandiamaklarna"
email_ending = "se"

unscraped = deque([original_url])

scraped = set()

emails = set()

# Här fuckade jag upp för jag satte 'original_url' där det skulle vara 'url'

while len(unscraped):
    url = unscraped.popleft()
    scraped.add(url)

    parts = urlsplit(url)

    base_url = "{0.scheme}://{0.netloc}".format(parts)

    if "/" in parts.path:
        path = url[: url.rfind("/") + 1]
    else:
        path = url

    print("Crawling URL %s" % url)
    try:
        response = requests.get(url)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        continue

    soup = BeautifulSoup(response.text, "lxml")

    spam_span = soup.find("span", {"class": "spamspan"}) if not None else None
    if spam_span:
        spam_span = soup.find("span", {"class": "spamspan"})
        # this helped me discover how they were arranged:
        # for child in spam_span.contents:
        #     print(child.text)

        full_name = spam_span.contents[0].text
        # # [1] is the '[at]' thingy
        domain = spam_span.contents[2].text
        parsed_email = f"{full_name}@{domain}"
        print(parsed_email)
        emails.add(parsed_email)

    for anchor in soup.find_all("a"):
        if "href" in anchor.attrs:
            link = anchor.attrs["href"]
        else:
            link = ""

        if link.startswith(deep_link_starts_with) and link.endswith(
            deep_link_ends_with
        ):
            link = base_url + link
            print(link)

            if not link.endswith(".gz"):
                if not link in unscraped and not link in scraped:
                    unscraped.append(link)

        else:
            continue


df = pd.DataFrame(emails, columns=["email"])
df.to_csv(csv_name + ".csv", index=False)
