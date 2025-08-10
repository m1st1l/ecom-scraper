# ecom-scraper (Python, Requests, BeautifulSoup)

Parses product cards from https://books.toscrape.com and saves them to CSV.

## Setup
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

## Run
python scrape_books.py
# output: books.csv

## Notes
- polite crawling (0.5s delay), basic error handling
- easy to extend to new fields/sites
