"""Scrape işinin tüm parametrelerini tek bir tipli nesnede toplar."""
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse


@dataclass
class ScrapeConfig:
    url: str
    item_selector: str                       # Her kayıt kartını seçen CSS selector
    fields: dict[str, str]                   # {"title": "h3 a", "price": ".price_color"}
    next_selector: str | None = None         # Sonraki sayfa butonu (yoksa tek sayfa)
    out: Path = Path("output/result.xlsx")
    max_pages: int = 0                       # 0 = sınırsız
    headless: bool = True
    attrs: dict[str, str] = field(default_factory=dict)  # {"url": "href"} gibi attribute okuma

    def validate(self) -> None:
        parsed = urlparse(self.url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise ValueError(f"Geçersiz URL: {self.url}")
        if not self.fields:
            raise ValueError("En az bir --field gerekli.")
        if self.out.suffix.lower() not in (".xlsx", ".json", ".csv"):
            raise ValueError("--out uzantısı .xlsx, .json veya .csv olmalı.")