"""Tarayıcıdan bağımsız, unit test edilebilir yardımcı fonksiyonlar."""
import re
from urllib.parse import urljoin


def parse_price(text: str | None) -> float | None:
    """'£51.77', '$1,299.00', '1.299,00 ₺', '€ 12,5' -> float. Parse edilemezse None."""
    if not text:
        return None
    s = re.sub(r"[^\d.,-]", "", text)          # para birimi ve boşlukları at
    if not re.search(r"\d", s):
        return None

    if "," in s and "." in s:
        # Sonda olan ayraç ondalıktır, diğeri binlik ayraçtır
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        head, _, tail = s.rpartition(",")
        # '1,299' -> binlik, '12,5' / '12,50' -> ondalık
        s = head.replace(",", "") + tail if len(tail) == 3 else head.replace(",", "") + "." + tail
    elif s.count(".") > 1:                       # '1.299.000' -> binlik
        s = s.replace(".", "")

    try:
        return float(s)
    except ValueError:
        return None


def absolute_url(base: str, href: str | None) -> str | None:
    """Göreli link (../x, /x, x.html) -> mutlak URL."""
    return urljoin(base, href) if href else None