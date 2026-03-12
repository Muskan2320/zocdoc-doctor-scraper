# Zocdoc Doctor Scraper

A Python-based web scraper that collects doctor listing data from Zocdoc across multiple cities.

## Features

- Scrapes doctor listings from multiple cities
- Handles pagination automatically
- Extracts structured provider information
- Avoids duplicate entries
- Handles missing fields gracefully
- Exports results to CSV

## Extracted Data

The scraper collects:

- Profile Image URL
- Doctor Name
- Profile URL
- Specialty
- Rating
- Review Count

## Installation

Clone the repository

git clone https://github.com/yourusername/zocdoc-doctor-scraper.git

Navigate to the project

cd zocdoc-doctor-scraper

Install dependencies

pip install -r requirements.txt

Install Playwright browser

playwright install

## Usage

Run the scraper:

python scraper.py

## Output

Results are saved in:

output/zocdoc_doctors.csv

## Tech Stack

- Python
- Playwright
- Pandas