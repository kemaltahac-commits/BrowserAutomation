import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from parsing import absolute_url, parse_price


@pytest.mark.parametrize("raw, expected", [
    ("£51.77", 51.77),
    ("$1,299.00", 1299.00),
    ("1.299,00 ₺", 1299.00),
    ("€ 12,5", 12.5),
    ("1,299", 1299.0),
    ("1.299.000", 1299000.0),
    ("Ücretsiz", None),
    ("", None),
    (None, None),
])
def test_parse_price(raw, expected):
    assert parse_price(raw) == expected


def test_absolute_url():
    base = "https://books.toscrape.com/catalogue/page-2.html"
    assert absolute_url(base, "a-light_1000/index.html") == \
        "https://books.toscrape.com/catalogue/a-light_1000/index.html"
    assert absolute_url(base, "../index.html") == "https://books.toscrape.com/index.html"
    assert absolute_url(base, None) is None