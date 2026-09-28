import csv
import sqlite3

CSV_FILE = "books.csv"
DB_FILE = "books.db"

connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS books")

cursor.execute("""
CREATE TABLE books (
    title TEXT NOT NULL,
    price REAL NOT NULL,
    rating INTEGER NOT NULL,
    in_stock INTEGER NOT NULL,
    url TEXT NOT NULL
)
""")

with open(CSV_FILE, newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    rows = [
        (
            row["title"],
            float(row["price"]),
            int(row["rating"]),
            1 if row["in_stock"].lower() == "true" else 0,
            row["url"],
        )
        for row in reader
    ]

cursor.executemany("""
INSERT INTO books (title, price, rating, in_stock, url)
VALUES (?, ?, ?, ?, ?)
""", rows)

connection.commit()

count = cursor.execute("SELECT COUNT(*) FROM books").fetchone()[0]
print(f"Loaded {count} books into {DB_FILE}")

connection.close()
