# DecaScraper
Decathlon Web Scraping Project.

## Project description
This project is a part of a bigger purpose. The file `scraper.py` contains all the source code generated to scrap data from www.decathlon.es/es. The data will be later exploited in order to obtain conclusions from it. The scrapped data includes:
- **products**: Price, name, description, discount etc... Identified bye a unique ID.
- **product_reviews**: author data, text, rating, usage, product id.
- **product_characteristics**: title , description, product_id.

## Project structure
- The folder `data/` contains the scrapped data in *.csv* format.

## Usage:
Run: `python -m scraper *<queries> --get <information>`.
Example: `python -m scraper balón zapatillas --get products`.
Example 2: `python -m scraper camiseta --get reviews`. 