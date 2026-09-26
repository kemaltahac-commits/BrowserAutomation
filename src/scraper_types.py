class Scraper:
    
    def scrape(self):
        print("Genel scraper çalışıyor")


class BookScraper(Scraper):

    def scrape(self):
        print("Kitaplar scrape ediliyor")


class ProductScraper(Scraper):

    def scrape(self):
        print("Ürünler scrape ediliyor")