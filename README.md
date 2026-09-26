# Browser Automation & Web Scraper

A Python-based browser automation and web scraping project built with Playwright and Pandas.

This project automatically navigates through a paginated website, extracts structured product information, processes the data, and exports the results to Excel.

## Problem

Manually collecting product information from multiple web pages is repetitive and time-consuming.

This project automates the process by navigating through available pages, extracting product data, processing it with Pandas, and generating an Excel report.

## Features

- Browser automation with Playwright
- Automated product scraping
- Pagination handling
- Product title extraction
- Price extraction and numeric conversion
- Absolute URL normalization
- Pandas data processing
- Excel report generation
- Error-safe browser cleanup
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
│   ├── automation.py
│   ├── main.py
│   ├── reporter.py
│   ├── scraper.py
│   └── scraper_types.py
│
├── tests/
│   └── test_scraper.py
│
├── .gitignore
└── README.md
How It Works

The scraper follows this workflow:

Website
   ↓
Playwright Browser Automation
   ↓
Pagination
   ↓
Product Extraction
   ↓
URL Normalization
   ↓
Price Conversion
   ↓
Pandas DataFrame
   ↓
Excel Report
   ↓
Automated Tests
Installation

Clone the repository:

git clone https://github.com/kemaltahac-commits/BrowserAutomation.git
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
Convert prices to numeric values.
Convert relative URLs into absolute URLs.
Store the collected data in a Pandas DataFrame.
Calculate basic price statistics.
Export the results to Excel.
Close the browser safely.

The current run processes 1000 products.

The generated Excel file will be saved to:

output/all_books.xlsx
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
Output Statistics

The scraper calculates basic price statistics:

Total products: 1000
Average price: 35.07
Highest price: 59.99
Lowest price: 10.00
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
Error Handling

The automation system uses a try/finally structure to ensure that the browser is closed even if an error occurs during scraping or report generation.

This prevents browser resources from remaining open after a failed execution.

OOP Structure

The project also demonstrates:

Composition
Inheritance
Polymorphism
Separation of responsibilities

The main automation flow is separated into:

AutomationSystem
       │
       ├── BookScraper
       │
       └── ReportGenerator
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