# Browser Automation & Web Scraper

A Python-based browser automation and web scraping project built with Playwright and Pandas.

The project automatically navigates through a paginated website, extracts product information, processes the collected data, and exports the results to Excel.

## Features

- Browser automation with Playwright
- Automated product scraping
- Pagination handling
- Product title extraction
- Price extraction and conversion
- Absolute URL normalization
- Pandas data processing
- Excel report generation
- Error handling
- Logging
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
│
├── output/
│   └── all_books.xlsx
│
├── logs/
│   └── scraper.log
│
├── src/
│   └── main.py
│
├── tests/
│   └── test_scraper.py
│
├── .gitignore
├── README.md
└── venv/ 

How It Works

The scraper follows this workflow:

Website
   ↓
Playwright Browser Automation
   ↓
Product Extraction
   ↓
Pagination
   ↓
URL Normalization
   ↓
Pandas DataFrame
   ↓
Data Processing
   ↓
Excel Report
   ↓
Logging & Testing 

Installation

Clone the repository:

git clone <YOUR_REPOSITORY_URL>
cd BrowserAutomation

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install dependencies:

pip install playwright pandas openpyxl pytest

Install the Chromium browser required by Playwright:

playwright install chromium
Run the Scraper

From the project root:

py src/main.py

The scraper will:

Open the target website.
Navigate through available pages.
Extract product titles, prices, and URLs.
Convert relative URLs into absolute URLs.
Store the data in a Pandas DataFrame.
Calculate basic price statistics.
Export the results to Excel.
Write execution information to the log file.

The generated Excel file will be saved to:

output/all_books.xlsx

Logs will be saved to:

logs/scraper.log
Testing

Run the automated tests with:

py -m pytest tests

The test suite verifies:

Excel output exists
Excel contains data
Required columns exist
Prices are numeric
URLs are absolute
Product titles are not empty

Current test result:

6 passed
Example Output

The generated dataset contains:

Column	Description
title	Product title
price	Product price as a numeric value
url	Absolute product URL

Example:

title: A Light in the Attic
price: 51.77
url: https://books.toscrape.com/...
Error Handling & Logging

The scraper uses Python's logging module to record:

Scraping start/end
Page processing
Product counts
Scraping errors
Report generation
Output creation
Browser shutdown

If an individual product cannot be scraped, the error is logged and the scraper continues processing the remaining products.

Purpose

This project was built as a practical browser automation and data processing project.

It demonstrates the ability to combine:

Browser Automation + Web Scraping + Data Processing + Excel Reporting + Testing

The architecture can be extended for business automation workflows such as:

Product data collection
Price monitoring
Business data extraction
Automated Excel reports
Website-to-Excel workflows
Recurring data collection
Author

Kemal

Management Information Systems Student
Python Automation & Business Data Tools