# Browser Automation & Web Scraper

A Python browser automation and web scraping tool built with Playwright and Pandas. It navigates paginated websites, extracts structured data, cleans it, and exports to Excel, CSV or JSON. It can be configured entirely from the command line.

## Problem

Collecting data from many web pages by hand is repetitive and slow. This project automates it: point it at a URL, describe what to extract with CSS selectors, and get a clean data file.

## Features

- Configurable scraping from the CLI (no code changes per site)
- Pagination handling via a next-page selector
- Field extraction by CSS selector or attribute (`selector@attr`)
- Safe price parsing (`£51.77`, `$1,299.00`, `1.299,00 ₺`, `€ 12,5`)
- Relative to absolute URL normalization
- Export to `.xlsx`, `.csv` or `.json`
- Input validation and clear exit codes
- Browser cleanup with try/finally
- 16 automated tests with Pytest

## Tech Stack

Python, Playwright, Pandas, OpenPyXL, Pytest

## Project Structure

```text
BrowserAutomation/
├── output/              # generated data files
├── logs/                # log files
├── src/
│   ├── cli.py           # command-line entry point
│   ├── config.py        # scrape configuration and validation
│   ├── engine.py        # scraping orchestration (pagination, extraction)
│   ├── parsing.py       # price and URL normalization (unit-tested)
│   ├── automation.py    # legacy flow: orchestrates scraper + report
│   ├── scraper.py       # legacy book scraper
│   ├── reporter.py      # legacy Excel report generator
│   └── main.py          # legacy entry point (books.toscrape.com)
├── tests/
│   ├── test_parsing.py  # unit tests for parsing
│   └── test_scraper.py  # checks on output/all_books.xlsx
├── .gitignore
└── README.md
```

## Installation

```bash
git clone https://github.com/kemaltahac-commits/BrowserAutomation.git
cd BrowserAutomation
python -m venv venv
```

Activate the environment:

```bash
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

Install dependencies and the browser:

```bash
pip install playwright pandas openpyxl pytest
playwright install chromium
```

## CLI Usage

```bash
py src/cli.py --url https://books.toscrape.com/ \
  --item-selector "article.product_pod" \
  --field title="h3 a@title" \
  --field price=".price_color" \
  --field url="h3 a@href" \
  --next-selector "li.next a" \
  --out output/books.xlsx
```
Option	Description
--url	Start URL (must be a valid URL)
--item-selector	CSS selector matching each record on the page
--field NAME=SELECTOR[@ATTR]	Field to extract. Repeatable. @attr reads an attribute (e.g. @href, @title)
--next-selector	Selector of the next-page link. Without it, one page is scraped
--max-pages	Limit the number of pages
--out	Output file. Extension must be .xlsx, .json or .csv
Exit codes:

Code	Meaning
0	Success
2	Invalid arguments (bad URL, bad output extension)
3	Zero records scraped (check selectors)
Example run (full site):

text
Copy
Sayfa 50: 20 kayıt (toplam 1000)
Bitti: 1000 kayıt -> output\books.xlsx
Try:
|
Legacy Flow
The original fixed-target flow is still available:

bash
Copy
py src/main.py
Try:
|
It scrapes all 1000 books from books.toscrape.com and writes output/all_books.xlsx with basic price statistics (average 35.07, max 59.99, min 10.00).

Output Format
Column	Description
title	Product title
price	Price as a numeric value
url	Absolute product URL
Column names come from the --field names you provide.

Testing
bash
Copy
py -m pytest tests -v
Try:
|
Current result: 16 passed.

test_parsing.py: price formats (£, $, €, ₺, thousands separators, text, empty, None) and absolute URL resolution.
test_scraper.py: output file exists, contains data, required columns exist, prices are numeric, URLs are absolute, titles are not empty.
Note: test_scraper.py reads output/all_books.xlsx, so run py src/main.py first on a fresh clone.

Error Handling
Invalid URL or output extension fails fast with exit code 2.
A wrong --item-selector logs a warning and exits with code 3.
The browser is closed in a finally block even if scraping fails.
Use Cases
Product data collection
Price monitoring
Website-to-Excel workflows
Recurring data extraction for business reports
Author
Kemal
Management Information Systems Student
Python Automation & Business Data Tools