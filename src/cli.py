"""Komut satırı giriş noktası.

Örnek (PowerShell, tek satır):
py src/cli.py --url https://books.toscrape.com/ --item-selector "article.product_pod" --field title="h3 a@title" --field price=".price_color" --field url="h3 a@href" --next-selector "li.next a" --out output/books.xlsx
"""
import argparse
import logging
import sys
from pathlib import Path

from config import ScrapeConfig
from engine import scrape, write_output


def parse_field(raw: str) -> tuple[str, str, str | None]:
    """'name=selector' veya 'name=selector@attr' formatını ayrıştırır.

    'title=h3 a@title'   -> ('title', 'h3 a', 'title')
    'price=.price_color' -> ('price', '.price_color', None)
    """
    if "=" not in raw:
        raise argparse.ArgumentTypeError(
            f"Hatalı --field: '{raw}'. Format: name=selector veya name=selector@attr"
        )
    name, _, rest = raw.partition("=")
    name, rest = name.strip(), rest.strip()
    if not name or not rest:
        raise argparse.ArgumentTypeError(f"Boş alan: '{raw}'")

    selector, sep, attr = rest.rpartition("@")
    # attr geçerli bir attribute adı gibi görünmeli (a[href*="@"] gibi selector'ları bozmasın)
    if sep and attr.replace("-", "").replace("_", "").isalnum():
        return name, selector.strip(), attr.strip()
    return name, rest, None


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="scraper-cli",
        description="Parametrik web scraper: herhangi bir siteyi Excel/JSON/CSV'ye çevirir.",
    )
    p.add_argument("--url", required=True, help="Başlangıç URL'si")
    p.add_argument("--item-selector", required=True,
                   help="Her kaydı saran CSS selector (örn. article.product_pod)")
    p.add_argument("--field", action="append", required=True, type=parse_field,
                   metavar="NAME=SELECTOR[@ATTR]",
                   help="Çekilecek alan. Birden fazla kez kullanılabilir.")
    p.add_argument("--next-selector", default=None,
                   help="Sonraki sayfa butonu selector'ı (verilmezse tek sayfa)")
    p.add_argument("--out", type=Path, default=Path("output/result.xlsx"),
                   help="Çıktı dosyası (.xlsx/.json/.csv)")
    p.add_argument("--max-pages", type=int, default=0,
                   help="Maksimum sayfa sayısı (0 = sınırsız)")
    p.add_argument("--headed", action="store_true",
                   help="Tarayıcıyı görünür aç (debug için)")
    p.add_argument("-v", "--verbose", action="store_true", help="DEBUG logları")
    return p


def setup_logging(verbose: bool) -> None:
    Path("logs").mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("logs/scraper.log", encoding="utf-8"),
        ],
    )


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    setup_logging(args.verbose)
    log = logging.getLogger("cli")

    fields = {name: sel for name, sel, _ in args.field}
    attrs = {name: attr for name, _, attr in args.field if attr}

    cfg = ScrapeConfig(
        url=args.url,
        item_selector=args.item_selector,
        fields=fields,
        attrs=attrs,
        next_selector=args.next_selector,
        out=args.out,
        max_pages=args.max_pages,
        headless=not args.headed,
    )

    try:
        cfg.validate()
    except ValueError as e:
        log.error(e)
        return 2

    log.info("Başlıyor: %s", cfg.url)
    try:
        rows = scrape(cfg)
    except Exception:
        log.exception("Scraping başarısız")
        return 1

    if not rows:
        log.error("0 kayıt çekildi. --item-selector / --field değerlerini kontrol et.")
        return 3

    write_output(rows, cfg.out)
    log.info("Bitti: %d kayıt -> %s", len(rows), cfg.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())