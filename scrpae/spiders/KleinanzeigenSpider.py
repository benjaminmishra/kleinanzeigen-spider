import scrapy
from scrpae.items import House

class KleinanzeigenSpider(scrapy.Spider):
    name = "kleinanzeigen_houses"

    def start_requests(self):
        start_urls = self.settings.getlist("START_URLS")
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        houses_records = response.css('div.aditem-main')
        for house_record in houses_records:
            link = house_record.css('a.ellipsis::attr(href)').get()
            yield response.follow(link, self.parse_link)

        # Follow pagination link
        next_page = response.css('a.pagination-page::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_link(self, response):
        house = House()
        house['price'] = response.css('#viewad-price::text').get().strip()
        house['location'] = response.css('#viewad-locality::text').get().strip();
        house['grundstuck'] = self.extract_with_default(
            selector=response,
            xpath_query = '//li[contains(text(), "Grundstücksfläche")]/span/text()',
            default = 0.0,
            post_process=self.strip_metersquare
        )
        house['zimmer_count'] = self.extract_with_default(
            selector=response,
            xpath_query = '//li[contains(text(), "Zimmer")]/span/text()',
            default = 0,
        )
        house['description'] = response.css('#viewad-description-text').get()
        house['link'] = response.url
        return house

    def extract_with_default(self,selector, xpath_query, default=None, post_process=None):
        """
        Extracts text from the given selector using an XPath query.
        Applies a post-processing function if provided.
        Returns the extracted text or a default value if no text is found.

        Args:
            selector (scrapy.Selector): The selector to apply the XPath to.
            xpath_query (str): The XPath query string.
            default (str, optional): The default value to return if no data is extracted. Defaults to ''.
            post_process (function, optional): A function to apply to the extracted text. Defaults to None.
        """
        extracted = selector.xpath(xpath_query).get()
        if extracted is None:
            return default
        if post_process:
            return post_process(extracted)
        return extracted.strip()

    def strip_metersquare(self, text):
        return text.strip('m²').strip()
