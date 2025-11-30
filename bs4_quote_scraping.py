import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://quotes.toscrape.com/"


def get_soup(url):
    """Fetch a URL and return a BeautifulSoup object."""
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def scrape_author_details(author_url):
    """Visit the author's page and extract biography information."""
    soup = get_soup(author_url)

    name = soup.find("h3", class_="author-title").text.strip()
    birth_date = soup.find("span", class_="author-born-date").text.strip()
    birth_location = soup.find("span", class_="author-born-location").text.strip()
    description = soup.find("div", class_="author-description").text.strip()

    return {
        "name": name,
        "birth_date": birth_date,
        "birth_location": birth_location,
        "description": description
    }


def scrape_quotes():
    """Scrape all quotes across all pages, including author info."""
    quotes_data = []
    authors_data = {}
    page_url = BASE_URL

    while True:
        soup = get_soup(page_url)
        quotes = soup.find_all("div", class_="quote")

        for q in quotes:
            quote_text = q.find("span", class_="text").text.strip()
            author = q.find("small", class_="author").text.strip()
            tags = [tag.text for tag in q.find_all("a", class_="tag")]

            author_relative_url = q.find("a")["href"]
            author_url = BASE_URL.rstrip("/") + author_relative_url

            if author not in authors_data:
                print(f"Scraping author details: {author_url}")
                authors_data[author] = scrape_author_details(author_url)
                time.sleep(0.5)

            quotes_data.append({
                "quote": quote_text,
                "author": author,
                "tags": ", ".join(tags),
                "author_page": author_url
            })

        next_btn = soup.find("li", class_="next")
        if not next_btn:
            break

        next_page = next_btn.find("a")["href"]
        page_url = BASE_URL + next_page

        time.sleep(0.5)

    return quotes_data, authors_data


def save_to_csv(quotes_data, authors_data):
    """Save quotes.csv and authors.csv."""
    with open("quotes.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Quote", "Author", "Tags", "Author Page"])

        for q in quotes_data:
            writer.writerow([q["quote"], q["author"], q["tags"], q["author_page"]])

    with open("authors.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Birth Date", "Birth Location", "Description"])

        for author, info in authors_data.items():
            writer.writerow([
                info["name"],
                info["birth_date"],
                info["birth_location"],
                info["description"]
            ])


def main():
    print("Starting scrape...")
    quotes_data, authors_data = scrape_quotes()
    save_to_csv(quotes_data, authors_data)
    print("Scraping complete. Data saved to quotes.csv and authors.csv")


if __name__ == "__main__":
    main()
