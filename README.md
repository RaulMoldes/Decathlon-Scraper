# DecaScraper

Decathlon Web Scraping Project. This project is a web scraper that extracts data from the website: `https://www.decathlon.es/es` and saves it to a csv file.
The data can be used later for knowledge discovery purposes.

## Project description

This project is a part of a bigger purpose. The file `scraper.py` contains all the source code generated to scrap data from decathlon website. The scrapped data includes:

- **products**: Price, name, description, discount etc... Identified bye a unique ID.
- **product_reviews**: author data, text, rating, usage, product id.
- **product_characteristics**: title , description, product_id.

## Project structure

- The `scraper.py` file contains all the source code.
- The folder `data/` contains the scrapped data in _.csv_ format.

## Usage:

- Scraper module:
  - Run: `python -m scraper *<queries> --get <information>`.
  - Example: `python -m scraper balón zapatillas --get products`.
  - Example 2: `python -m scraper camiseta --get reviews`.
  - Example 3: `python -m scraper portería --get characteristics.`
