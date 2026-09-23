import logging
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
from playwright.sync_api import sync_playwright


# =========================
# KLASÖRLER
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)


# =========================
# LOGGING
# =========================

LOG_FILE = LOG_DIR / "scraper.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# =========================
# SCRAPER
# =========================

def scrape_books():
    products_data = []

    page_number = 1

    with sync_playwright() as p:

        browser = None

        try:
            logger.info("Scraping başladı.")

            browser = p.chromium.launch(headless=False)

            page = browser.new_page()

            page.goto(
                "https://books.toscrape.com/",
                wait_until="domcontentloaded"
            )

            while True:

                logger.info(f"Sayfa {page_number} işleniyor...")
                print(f"Scraping page {page_number}...")

                try:

                    products = page.locator("article.product_pod")

                    product_count = products.count()

                    logger.info(
                        f"Sayfa {page_number}: {product_count} ürün bulundu."
                    )

                    for index, product in enumerate(products.all(), start=1):

                        try:

                            title = product.locator(
                                "h3 a"
                            ).get_attribute("title")

                            price = product.locator(
                                ".price_color"
                            ).inner_text()

                            url = product.locator(
                                "h3 a"
                            ).get_attribute("href")

                            # Relative URL → Absolute URL
                            url = urljoin(page.url, url)

                            products_data.append({
                                "title": title,
                                "price": price,
                                "url": url
                            })

                        except Exception as e:

                            logger.error(
                                f"Sayfa {page_number}, "
                                f"ürün {index} scrape edilemedi: {e}"
                            )

                            continue

                except Exception as e:

                    logger.error(
                        f"Sayfa {page_number} işlenirken hata oluştu: {e}"
                    )

                # =========================
                # NEXT PAGE
                # =========================

                try:

                    next_button = page.locator("li.next a")

                    if next_button.count() == 0:

                        logger.info(
                            "Son sayfaya ulaşıldı."
                        )

                        break

                    next_button.click()

                    page_number += 1

                except Exception as e:

                    logger.error(
                        f"Sonraki sayfaya geçerken hata oluştu: {e}"
                    )

                    break

        except Exception as e:

            logger.exception(
                f"Scraper kritik bir hata nedeniyle durdu: {e}"
            )

        finally:

            if browser:

                browser.close()

                logger.info("Browser kapatıldı.")

    return products_data


# =========================
# DATA PROCESSING
# =========================

def create_report(products_data):

    if not products_data:

        logger.warning(
            "Hiç ürün verisi bulunamadı."
        )

        return

    try:

        df = pd.DataFrame(products_data)

        # Price temizleme
        df["price"] = (
            df["price"]
            .str.replace("£", "", regex=False)
            .astype(float)
        )

        # =========================
        # ANALYSIS
        # =========================

        average_price = df["price"].mean()

        max_price = df["price"].max()

        min_price = df["price"].min()

        print("\nScraping tamamlandı.")

        print("Toplam ürün:", len(df))

        print("Ortalama fiyat:", average_price)

        print("En pahalı:", max_price)

        print("En ucuz:", min_price)

        logger.info(
            f"Toplam ürün: {len(df)}"
        )

        logger.info(
            f"Ortalama fiyat: {average_price:.2f}"
        )

        logger.info(
            f"En pahalı: {max_price:.2f}"
        )

        logger.info(
            f"En ucuz: {min_price:.2f}"
        )

        # =========================
        # EXCEL
        # =========================

        output_file = OUTPUT_DIR / "all_books.xlsx"

        df.to_excel(
            output_file,
            index=False
        )

        print(
            f"\nExcel oluşturuldu: {output_file}"
        )

        logger.info(
            f"Excel oluşturuldu: {output_file}"
        )

    except Exception as e:

        logger.exception(
            f"Rapor oluşturulurken hata oluştu: {e}"
        )

        print(
            f"\nRapor oluşturulurken hata oluştu: {e}"
        )


# =========================
# MAIN
# =========================

if __name__ == "__main__":

    logger.info("=" * 50)
    logger.info("BOOK SCRAPER BAŞLATILDI")
    logger.info("=" * 50)

    products = scrape_books()

    create_report(products)

    logger.info("=" * 50)
    logger.info("BOOK SCRAPER TAMAMLANDI")
    logger.info("=" * 50)

    input("\nKapatmak için Enter'a bas...")