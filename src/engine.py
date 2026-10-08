"""Parametrik scraping motoru: ScrapeConfig -> list[dict]."""
import json
import logging
from pathlib import Path

import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

from config import ScrapeConfig
from parsing import absolute_url, parse_price

log = logging.getLogger("engine")

NAV_TIMEOUT_MS = 30_000
ITEM_TIMEOUT_MS = 10_000
RETRIES = 3
URL_ATTRS = {"href", "src"}      # bu attribute'lar mutlak URL'ye çevrilir

# Sayfadaki tüm kartları tek seferde okuyan JS (alan başına ayrı round-trip yok)
_JS_EXTRACT = """
(els, spec) => els.map(el => {
    const row = {};
    for (const [name, cfg] of Object.entries(spec)) {
        const node = el.querySelector(cfg.sel);
        row[name] = !node ? null
            : cfg.attr ? node.getAttribute(cfg.attr)
            : node.innerText.trim();
    }
    return row;
})
"""


def _goto(page, url: str) -> None:
    """Retry'lı navigasyon."""
    for attempt in range(1, RETRIES + 1):
        try:
            page.goto(url, timeout=NAV_TIMEOUT_MS, wait_until="domcontentloaded")
            return
        except PWTimeout:
            log.warning("goto başarısız (%d/%d): %s", attempt, RETRIES, url)
            if attempt == RETRIES:
                raise


def _extract_page(page, cfg: ScrapeConfig) -> list[dict]:
    spec = {n: {"sel": s, "attr": cfg.attrs.get(n)} for n, s in cfg.fields.items()}
    rows = page.locator(cfg.item_selector).evaluate_all(_JS_EXTRACT, spec)

    for row in rows:
        # href/src alanlarını mutlak URL'ye çevir
        for name, attr in cfg.attrs.items():
            if attr in URL_ATTRS:
                row[name] = absolute_url(page.url, row.get(name))
        # "price" ile biten alanları sayıya çevir
        for name in row:
            if name.lower().endswith("price"):
                raw = row[name]
                row[name] = parse_price(raw)
                if raw and row[name] is None:
                    log.warning("Fiyat parse edilemedi: %r", raw)
    return rows


def scrape(cfg: ScrapeConfig) -> list[dict]:
    results: list[dict] = []
    seen: set[str] = set()

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=cfg.headless)
        try:
            page = browser.new_page()
            _goto(page, cfg.url)
            page_no = 0

            while True:
                if page.url in seen:
                    log.warning("Aynı sayfaya geri dönüldü, döngü kesiliyor: %s", page.url)
                    break
                seen.add(page.url)
                page_no += 1

                try:
                    page.wait_for_selector(cfg.item_selector, timeout=ITEM_TIMEOUT_MS)
                except PWTimeout:
                    log.warning("Sayfa %d: item_selector bulunamadı (%s)", page_no, page.url)
                    break

                rows = _extract_page(page, cfg)
                results.extend(rows)
                log.info("Sayfa %d: %d kayıt (toplam %d)", page_no, len(rows), len(results))

                if cfg.max_pages and page_no >= cfg.max_pages:
                    break
                if not cfg.next_selector:
                    break

                nxt = page.locator(cfg.next_selector)
                if nxt.count() == 0:
                    break
                href = nxt.first.get_attribute("href")
                if href:
                    _goto(page, absolute_url(page.url, href))
                else:                                   # JS butonu: tıkla
                    nxt.first.click()
                    page.wait_for_load_state("domcontentloaded")
        finally:
            browser.close()

    return results


def write_output(rows: list[dict], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    ext = out.suffix.lower()
    if ext == ".xlsx":
        df.to_excel(out, index=False)
    elif ext == ".csv":
        df.to_csv(out, index=False, encoding="utf-8-sig")
    else:
        out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")