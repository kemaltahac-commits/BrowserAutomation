# Browser Automation & Web Scraper

A configurable Python CLI tool for browser automation and web scraping. Built with Playwright and Pandas, it navigates paginated websites, extracts structured data with CSS selectors, cleans selected values, and exports results to Excel, CSV, or JSON.

## Problem

Collecting data from many web pages by hand is repetitive and slow. This project automates the workflow: provide a URL, describe the records and fields with CSS selectors, and receive a structured data file.

## Features

- Configurable scraping from the command line; no code changes required per site
- Pagination handling through a next-page selector
- Field extraction by CSS selector or HTML attribute (`selector@attr`)
- Price parsing for common currency and number formats
- Relative-to-absolute URL normalization for `href` and `src` fields
- Export to `.xlsx`, `.csv`, or `.json`
- Input validation and clear exit codes
- Browser cleanup with `try/finally`
- Automated tests with Pytest

## Tech Stack

- Python
- Playwright
- Pandas
- OpenPyXL
- Pytest

## Project Structure

```text
BrowserAutomation/
├── output/              # Generated data files
├── logs/                # Log files
├── src/
│   ├── cli.py           # Command-line entry point
│   ├── config.py        # Scrape configuration and validation
│   ├── engine.py        # Scraping orchestration, pagination, extraction
│   ├── parsing.py       # Price and URL normalization
│   ├── automation.py    # Legacy scraper and report flow
│   ├── scraper.py       # Legacy book scraper
│   ├── reporter.py      # Legacy Excel report generator
│   └── main.py          # Legacy entry point
├── tests/
│   ├── test_parsing.py
│   └── test_scraper.py
├── .gitignore
└── README.md
```

## Installation

```bash
git clone https://github.com/kemaltahac-commits/BrowserAutomation.git
cd BrowserAutomation
python -m venv venv
```

Activate the virtual environment:

```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# macOS / Linux
source venv/bin/activate
```

Install the dependencies and Chromium browser:

```bash
pip install playwright pandas openpyxl pytest
playwright install chromium
```

## CLI Usage

```text
scraper-cli --url URL --item-selector SELECTOR --field NAME=SELECTOR --out OUTPUT_FILE
```

### Arguments

Argument	Description
--url	-Start URL. Must be a valid URL.
--item-selector	CSS selector matching each record on the page.
--field-	Field to extract in NAME=SELECTOR[@ATTR] format. Repeatable.
--next-selector	CSS selector for the next-page link. Omit for a single-page scrape.
--max-pages	Optional limit for the number of pages.
--out-	Output file. Supported extensions: .xlsx, .csv, .json.
--headed-	Runs the browser with a visible window for inspection.

Demo 1: Books to Scrape

This demo scrapes the public practice site Books to Scrape and exports 1,000 book records.

.\venv\Scripts\python.exe .\src\cli.py `
  --url "https://books.toscrape.com/" `
  --item-selector "article.product_pod" `
  --field title="h3 a@title" `
  --field price=".price_color" `
  --field url="h3 a@href" `
  --next-selector "li.next a" `
  --out "output\all_books.xlsx"

  Expected result: Bitti: 1000 kayıt -> output\all_books.xlsx

  Demo 2: Quotes to Scrape

  This demo scrapes the public practice site Quotes to Scrape and exports 100 quote records.

  .\venv\Scripts\python.exe .\src\cli.py `
  --url "https://quotes.toscrape.com/" `
  --item-selector ".quote" `
  --field quote=".text" `
  --field author=".author" `
  --field tags=".tag" `
  --next-selector "li.next a" `
  --out "output\quotes.xlsx"

  Expected result: Bitti: 100 kayıt -> output\quotes.xlsx

  Output Format 

  The output columns are determined by the --field arguments you provide.

  Column  Description
  title   Product title 
  price   Parsed price as a numeric value
  url     Absolute product URL

  Exit Codes 
  Code Meaning
  0    Successful run
  2    Invalid arguments, such as an invalid URL or unsupported output extension
  3    Zero records scraped; check the selectors

  Testing 
   
  Run the automated test suite: 
  .\venv\Scripts\python.exe -m pytest tests -v

  The project currently includes 16 automated tests covering price parsing, URL normalization, output validation, numeric prices, non-empty titles, and absolute URLs.

test_scraper.py reads output/all_books.xlsx. On a fresh clone, run the Books to Scrape demo before running the tests.
 
 Responsible Use
Use this tool only on websites where you have permission to collect data, or where the data is publicly accessible and collection complies with the website’s terms, applicable laws, rate limits, and privacy requirements.

Do not use it to collect personal, private, restricted, or authentication-protected data without explicit authorization.

Use Cases
*  Product data collection
*  Price monitoring
*  Website-to-Excel workflows
*  Recurring data extraction for business reports
*  Public catalog and directory research 

Author
Kemal
Management Information Systems Student
Python Automation & Business Data Tools