from urllib.parse import urljoin
from playwright.sync_api import sync_playwright


class BookScraper:

    def __init__(self, url):
        self.url = url
        self.playwright = None
        self.browser = None
        self.page = None

    def open(self):
        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=False
        )

        self.page = self.browser.new_page()
        self.page.goto(self.url)

        print("Browser açıldı.")
        print("Title:", self.page.title())

    def scrape_products(self):
        products_data = []

        while True:
            products = self.page.locator("article.product_pod")

            for product in products.all():

                title = product.locator(
                    "h3 a"
                ).get_attribute("title")

                price_text = product.locator(
                    ".price_color"
                ).inner_text()

                price = float(
                    price_text.replace("£", "")
                )

                href = product.locator(
                    "h3 a"
                ).get_attribute("href")

                url = urljoin(self.page.url, href)

                products_data.append({
                    "title": title,
                    "price": price,
                    "url": url
                })

            next_button = self.page.locator(
                "li.next a"
            )

            if next_button.count() == 0:
                break

            next_button.click()
            self.page.wait_for_load_state("domcontentloaded")

        return products_data

    def close(self):
        self.browser.close()
        self.playwright.stop()

        print("Browser kapatıldı.")