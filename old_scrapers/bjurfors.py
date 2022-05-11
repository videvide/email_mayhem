# https://medium.com/swlh/how-to-scrape-email-addresses-from-a-website-and-export-to-a-csv-file-c5d1becbd1a0

import re
import requests
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd

original_url = ""
deep_link_starts_with = ""
deep_link_ends_with = ""
csv_name = ""
email_ending = ""

unscraped = deque([original_url])

scraped = set()

emails = set()

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

    new_emails = set(
        re.findall(
            r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\." + email_ending,
            response.text,
            re.I,
        )
    )
    emails.update(new_emails)

    soup = BeautifulSoup(response.text, "lxml")

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
df.to_csv(f"./csv_files{csv_name}" + ".csv", index=False)
