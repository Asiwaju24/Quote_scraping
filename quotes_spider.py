import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes_spider"
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        """Parse quote listings and follow author links + pagination."""
        quotes = response.css("div.quote")

        for quote in quotes:
            text = quote.css("span.text::text").get()
            author_name = quote.css("small.author::text").get()
            tags = quote.css("a.tag::text").getall()
            author_page = quote.css("span a::attr(href)").get()

            # Follow author page for deeper data
            author_url = response.urljoin(author_page)
            yield response.follow(
                author_url,
                callback=self.parse_author,
                meta={
                    "quote": text,
                    "author": author_name,
                    "tags": tags,
                    "author_url": author_url,
                }
            )

        # Pagination
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response):
        """Extract detailed author information."""
        quote = response.meta["quote"]
        author = response.meta["author"]
        tags = response.meta["tags"]
        author_url = response.meta["author_url"]

        name = response.css("h3.author-title::text").get().strip()
        birth_date = response.css("span.author-born-date::text").get()
        birth_location = response.css("span.author-born-location::text").get()
        description = response.css("div.author-description::text").get().strip()

        yield {
            "quote": quote,
            "author": author,
            "tags": tags,
            "author_page": author_url,
            "author_full_name": name,
            "author_birth_date": birth_date,
            "author_birth_location": birth_location,
            "author_description": description,
                   }
