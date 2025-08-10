import csv
import time
from typing import Iterator, Dict, List
import requests
from bs4 import BeautifulSoup

BASE = "https://books.toscrape.com"

def fetch(url: str) -> BeautifulSoup:
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")

def parse_listing(page_soup: BeautifulSoup) -> Iterator[Dict[str, str]]:
    for art in page_soup.select("article.product_pod"):
        title = art.h3.a["title"].strip()
        price = art.select_one(".price_color").text.strip().lstrip("£")
        rel = art.h3.a["href"]
        link = (BASE + "/catalogue/" + rel.split("catalogue/")[-1]).replace("../", "")
        yield {"title": title, "price_gbp": price, "url": link}

def next_page(page_soup: BeautifulSoup) -> str | None:
    nxt = page_soup.select_one("li.next > a")
    if not nxt:
        return None
    rel = nxt["href"]
    return BASE + "/catalogue/" + rel

def crawl(pages: int = 3) -> List[Dict[str, str]]:
    data: List[Dict[str, str]] = []
    url = BASE + "/catalogue/page-1.html"
    for _ in range(pages):
        soup = fetch(url)
        data.extend(parse_listing(soup))
        url = next_page(soup)
        if not url:
            break
        time.sleep(0.5)
    return data

def save_csv(rows: List[Dict[str, str]], path: str) -> None:
    if not rows:
        return
    cols = ["title", "price_gbp", "url"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

if __name__ == "__main__":
    items = crawl(pages=3)
    save_csv(items, "books.csv")
    print(f"Saved {len(items)} rows to books.csv")
