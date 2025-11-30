Web Scraping Projects (BeautifulSoup & Scrapy)

This repository contains two complete web scraping projects built with different tools in Python.
Both projects use publicly available websites created specifically for scraping practice, so they are safe and legal to scrape.

The purpose of this repository is to demonstrate different scraping approaches, from simple HTML parsing with BeautifulSoup to building a full crawler using Scrapy.



1. Quotes Scraper (Scrapy)

This project uses Scrapy to crawl the entire Quotes to Scrape website.

It collects:

Quote text

Author

Tags

Author biography page URL

Author full details: name, birth date, birth location, and description


The spider follows all pagination pages and visits every author page to extract additional information.
All results can be exported to JSON, CSV, or any file type supported by Scrapy.

How to run

Step into the Scrapy project folder, then run:

scrapy crawl quotes_spider -o quotes.json

You can replace quotes.json with quotes.csv or any other format.

The spider file is located in:

quotes_scraper/spiders/quotes_spider.py


---

2. Books Scraper (BeautifulSoup)

This project uses Python’s Requests and BeautifulSoup libraries to scrape Books to Scrape.

It extracts:

Book title

Price

Availability

Product description

Star rating

Image URL

Category


The script also:

Handles pagination

Crawls all categories

Downloads all book cover images

Saves the complete dataset into a CSV file


How to run

Install dependencies:

pip install requests beautifulsoup4

Then run:

python scrape.py

After running, the script generates:

books_full_scrape.csv with all the scraped data

An images/ folder containing book covers grouped by category


The main script is located at:

scrape.py



Project Structure

.
├── scrape.py                       # BeautifulSoup book scraper
├── books_full_scrape.csv           # Generated after running the script
├── images/                         # Book cover downloads
│   ├── Travel/
│   ├── Mystery/
│   └── ...
├── quotes_scraper/                 # Scrapy project folder
│   ├── quotes_scraper/
│   │   ├── spiders/
│   │   │   └── quotes_spider.py
│   │   ├── items.py
│   │   ├── settings.py
│   │   └── ...
│   └── scrapy.cfg
└── README.md

