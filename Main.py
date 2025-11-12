import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import csv

BASE_URL = "https://news.google.com/showcase"

headers = {"User-Agent": "MyScraperBot/1.0 (+http://github.com/nicholastrimble)"
           }

def fetch(url):
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.text

def parse_html(html, base_url):
    soup = BeautifulSoup(html, "lxml")
    results = []

    for a in soup.select("article a[href]"):
        href = a["href"]
        full = urljoin(base_url, href)
        title = a.get_text(strip=True)
        results.append({"title": title, "url": full})
    return results

def main():
    html = fetch(BASE_URL)
    items = parse_html(html, BASE_URL)
    for i, it in enumerate(items,1):
        print(i, it["title"])
        print(" ", it["url"])
    time.sleep(1)



if __name__ == "__main__":
    main()