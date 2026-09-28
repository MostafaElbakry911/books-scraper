import csv
import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
OUTPUT_FILE = "books.csv"
PAGES_TO_SCRAPE = 5

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def get_soup(session, url):
    response = session.get(url, timeout=15)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def scrape_books():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (compatible; BooksToScrapeTask/1.0)"
    })

    books = []

    for page_number in range(1, PAGES_TO_SCRAPE + 1):
        page_url = (
            BASE_URL
            if page_number == 1
            else urljoin(BASE_URL, f"catalogue/page-{page_number}.html")
        )

        soup = get_soup(session, page_url)

        for book in soup.select("article.product_pod"):
            title_tag = book.select_one("h3 a")
            price_tag = book.select_one("p.price_color")
            rating_tag = book.select_one("p.star-rating")
            stock_tag = book.select_one("p.instock.availability")

            title = title_tag.get("title", "").strip()
            price_text = price_tag.get_text(strip=True)

            price_match = re.search(r"\d+(\.\d+)?", price_text)

            if not price_match:
                raise ValueError(f"Could not extract price: {price_text}")

            price = float(price_match.group())
        
            rating_word = next(
                (class_name for class_name in rating_tag.get("class", [])
                 if class_name in RATING_MAP),
                None,
            )
            rating = RATING_MAP[rating_word]
            in_stock = str(stock_tag is not None).lower()
            book_url = urljoin(page_url, title_tag.get("href"))

            books.append({
                "title": title,
                "price": price,
                "rating": rating,
                "in_stock": in_stock,
                "url": book_url,
            })

        # Be polite even though this demo site is intended for scraping.
        time.sleep(0.2)

    books = books[:100]

    if len(books) != 100:
        raise RuntimeError(f"Expected 100 books, but scraped {len(books)}.")

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["title", "price", "rating", "in_stock", "url"],
        )
        writer.writeheader()
        writer.writerows(books)

    print(f"Saved {len(books)} books to {OUTPUT_FILE}")


if __name__ == "__main__":
    scrape_books()
