from .scraper import QuoteScraper
from .logger import get_logger

from typing import TypedDict, List, NotRequired

class Quote(TypedDict):
    quote: str
    author: str
    tags: NotRequired[List[str]]

class QuoteManager:
    no_of_managers = 0

    def __init__(self, page_url: str):
        self.page_url = page_url
        self.scraper = QuoteScraper(page_url)
        self._quotes = self._init_quotes_from_page()

        QuoteManager.no_of_managers += 1

        self.logger = get_logger(f"quote_manager {QuoteManager.no_of_managers}")

    def _init_quotes_from_page(self) -> List[dict]:
        return list(self.scraper.get_page_data())
        
    def __repr__(self):
        return f"QuoteManager<Page URL: {self.page_url}>"

    @staticmethod
    def _is_valid_str(text: str) -> None:
        text = text.strip()

        if not text: raise ValueError("Input text cannot be empty.")

    def add_quote(self, quote: Quote):
        self.logger.info("Validating the input fields supplied.")

        self._is_valid_str(quote["quote"])
        self._is_valid_str(quote["author"])

        self.logger.info("Including only valid tags supplied.")

        tags = []
        if "tags" in quote:
            for tag in quote["tags"]:
                try:
                    self._is_valid_str(tag)
                except: pass
                else:
                    tags.append(tag)

        self.logger.info("Adding the quote to list.")

        self._quotes.append({ **quote, "tags": tags })

        self.logger.info("Quote added successfully in the list")

    def search_quote(self, quote_text: str):
        self._is_valid_str(quote_text)

        for quote in self._quotes:
            if quote["quote"] == quote_text:
                return quote

        self.logger.info(f"!!No Quote found with the given search text: {quote_text}.")

        return {}

    @property
    def all_quotes(self):
        return self._quotes
