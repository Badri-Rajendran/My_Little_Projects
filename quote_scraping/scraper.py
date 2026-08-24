import requests

from bs4 import BeautifulSoup
from collections import namedtuple

from .locators import Locators

class QuoteScraper:
    def __init__(self, page_url: str):
        self.page_url = page_url
        self.page_source = self.parsed_html
        self._sections = self._quote_sections

    def __repr__(self):
        return f"QuoteScraper<Page URL: {self.page_url}>"

    @property
    def parsed_html(self) -> BeautifulSoup:
        response = requests.get(self.page_url)
        return BeautifulSoup(response.text, "html.parser")

    @property
    def _quote_sections(self) -> list:
        sections = self.page_source.select(Locators.QUOTE_SECTION_LOCATOR)
        return sections

    @property
    def quotes(self) -> list:
        quotes = [section.select_one(Locators.QUOTE_LOCATOR) for section in self._sections]
        return quotes

    @property
    def authors(self) -> list:
        authors = [section.select_one(Locators.AUTHOR_LOCATOR) for section in self._sections]
        return authors

    @property
    def all_section_tags(self):
        all_section_tags = [ section.select(Locators.TAG_LOCATOR) for section in self._sections ]
        return all_section_tags

    def get_section_tags(self, tag_index: int):
        if tag_index < 0: raise ValueError("Tag Index cannot be less than 0.")

        all_section_tags = self.all_section_tags
        length = len(all_section_tags)

        if tag_index > length: raise ValueError(f"Tag Index cannot be greater than {length} for this page.")

        return all_section_tags[tag_index]

    @staticmethod
    def _retrieve_content(arr: list) -> list:
        result = [value.string for value in arr]
        return result

    def get_page_data(self):
        convert_to_dict = lambda data: {"quote": data.quote, "author": data.author, "tags": data.tags}

        QuoteSection = namedtuple("QuoteSection", ["quote", "author", "tags"])

        quotes = self._retrieve_content(self.quotes)
        authors = self._retrieve_content(self.authors)
        all_section_tags = [ self._retrieve_content(section_tags) for section_tags in self.all_section_tags]

        return map(lambda section: convert_to_dict(QuoteSection(*section)), zip(quotes, authors, all_section_tags))

    
    

    

        
