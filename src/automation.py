from scraper import BookScraper
from reporter import ReportGenerator


class AutomationSystem:

    def __init__(self, url):
        self.scraper = BookScraper(url)
        self.reporter = ReportGenerator()

    def run(self):
        self.scraper.open()

        try:
            products = self.scraper.scrape_products()
            self.reporter.create_report(products)
        finally:
            self.scraper.close()