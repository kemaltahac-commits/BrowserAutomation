from automation import AutomationSystem
from scraper_types import BookScraper, ProductScraper


# ==========================================
# 1. GERÇEK BROWSER AUTOMATION
# ==========================================

print("\n" + "=" * 50)
print("BROWSER AUTOMATION")
print("=" * 50)

system = AutomationSystem(
    "https://books.toscrape.com/"
)

system.run()


# ==========================================
# 2. INHERITANCE + POLYMORPHISM DEMO
# ==========================================

print("\n" + "=" * 50)
print("INHERITANCE + POLYMORPHISM")
print("=" * 50)

scrapers = [
    BookScraper(),
    ProductScraper()
]

for scraper in scrapers:
    scraper.scrape()