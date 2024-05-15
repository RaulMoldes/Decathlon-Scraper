# Decathlon Web Scraper

Decathlon Web Scraping Project. This project is a web scraper that extracts data from the website: `https://www.decathlon.es/es` and saves it to a csv file.
The data can be used later for knowledge discovery purposes.

## Project requirements

The project has been built using the WebDriver for Chrome. This WebDriver (`https://chromedriver.chromium.org/downloads`) requires Chrome version 114.
Also, you will need a python 3.11 environment with:

- selenium==4.20.0
- pandas==2.1.3

## Project description

The file `scraper.py` contains all the source code generated to scrap data from decathlon website. The scrapped data includes:

- **products**: Price, name, description, discount etc... Identified by a unique ID.
- **product_reviews**: author data, text, rating, usage, product id.
- **product_characteristics**: title , description, product_id.

## Project structure

- The `scraper.py` file contains all the source code.
- The folder `data/` contains the scrapped data in _.csv_ format.

## Usage:

- Scraper module: `py -m scraper.py --query <query> --max_workers <max_workers>`
  --query(str): The query to search for.
  --max_workers(int): The maximum number of parallel threads to use on each search. Each thread fetches a single url. Defaults to 10.

## Example:

`py -m scraper.py --query zapatillas --max_workers 20`
