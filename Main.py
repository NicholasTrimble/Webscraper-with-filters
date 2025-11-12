import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import csv

BASE_URL = "https://news.google.com/showcase"  # note: Google News often renders with JS
HEADERS = {"User-Agent": "MyScraperBot/1.0 (+http://github.com/nicholastrimble)"}

# normalize keywords to lower-case once
FILTER_WORDS = ["Trump", "AI", "Python", "machine learning", "TSA", "airport"]
FILTER_WORDS = [w.lower() for w in FILTER_WORDS]

def fetch(url):
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.text

def parse_html(html, base_url):
    soup = BeautifulSoup(html, "lxml")
    results = []
    # The selector here is generic — adjust to the site's markup.
    for a in soup.select("article a[href]"):
        href = a.get("href")
        if not href:
            continue
        full = urljoin(base_url, href)
        title = a.get_text(strip=True)
        if not title:
            continue
        results.append({"title": title, "url": full})
    return results

def filter_results(results, keywords):
    filtered = []
    seen_urls = set()
    for item in results:
        title_lower = item["title"].lower()
        if any(k in title_lower for k in keywords):
            url = item["url"]
            if url not in seen_urls:
                seen_urls.add(url)
                filtered.append(item)
    return filtered

def save_to_csv(items, filename):
    if not items:
        print("No items to save.")
        return
    fieldnames = ["title", "url"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(items)
    print(f"Saved {len(items)} results to {filename}")

def main():
    try:
        html = fetch(BASE_URL)
    except Exception as e:
        print("Failed to fetch:", e)
        return

    items = parse_html(html, BASE_URL)
    print(f"Scraped {len(items)} items total.")
    filtered = filter_results(items, FILTER_WORDS)
    print(f"Found {len(filtered)} items matching keywords: {FILTER_WORDS}")
    save_to_csv(filtered, "filtered_results.csv")
    time.sleep(1)

if __name__ == "__main__":
    main()
