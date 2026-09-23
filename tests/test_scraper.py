from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = PROJECT_ROOT / "output" / "all_books.xlsx"


def test_excel_exists():
    assert OUTPUT_FILE.exists()


def test_excel_has_data():
    df = pd.read_excel(OUTPUT_FILE)

    assert len(df) > 0


def test_required_columns_exist():
    df = pd.read_excel(OUTPUT_FILE)

    required_columns = {"title", "price", "url"}

    assert required_columns.issubset(df.columns)


def test_prices_are_numeric():
    df = pd.read_excel(OUTPUT_FILE)

    assert pd.api.types.is_numeric_dtype(df["price"])


def test_urls_are_absolute():
    df = pd.read_excel(OUTPUT_FILE)

    assert df["url"].str.startswith("https://").all()


def test_titles_are_not_empty():
    df = pd.read_excel(OUTPUT_FILE)

    assert df["title"].notna().all()
    assert (df["title"].str.strip() != "").all()