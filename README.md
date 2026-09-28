# Books to Scrape — Web Scraping & SQL Task

## Overview

This project collects the first 100 books from the first five pages of [Books to Scrape](https://books.toscrape.com/) using Python.

The scraped data is cleaned and stored in `books.csv`, then loaded into SQLite for SQL analysis.

### Collected fields

* `title` — Book title
* `price` — Numeric price value
* `rating` — Rating from 1 to 5
* `in_stock` — Boolean stock status
* `url` — Book URL

## Project Structure

```text
books-scraper/
│
├── scraper.py
├── books.csv
├── load_db.py
├── queries.sql
├── requirements.txt
└── README.md
```

## Technologies

* Python
* Requests
* BeautifulSoup
* CSV
* SQLite
* SQL

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the scraper

```bash
python scraper.py
```

The scraper collects the first 100 books from pages 1–5 and saves them to:

```text
books.csv
```

### 3. Load the data into SQLite

```bash
python load_db.py
```

This creates the SQLite database and loads the CSV data into the `books` table.

### 4. Run the SQL queries

The requested SQL analysis is available in:

```text
queries.sql
```

The queries answer:

1. Average price for each rating
2. The 5 most expensive books rated 4 or 5
3. Number of out-of-stock books per rating

## Task Reflection

The scraping itself was straightforward because Books to Scrape is specifically designed for scraping practice. The main part that required attention was converting the price into a numeric value and the rating from words into integers.

I also made sure the stock status was stored consistently as a boolean value so it could be easily analyzed in SQL.

If the website started blocking requests after 50 requests, I would reduce the request rate and add controlled delays and exponential backoff. I would also reuse the HTTP session, cache successful responses, and avoid unnecessary requests.

The implementation focuses on being simple, readable, and easy to maintain rather than unnecessarily complex.
