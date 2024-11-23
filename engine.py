# engine.py
#!/usr/bin/env python3

from src.scraper.driver import start_driver, quit_driver
from src.scraper.engine import scraping_engine
import argparse
from urllib.parse import urlparse
import re

def extract_domain(base_url):
    # Parse the base URL to extract the domain
    parsed_url = urlparse(base_url)
    domain = parsed_url.netloc
    return domain


def extract_output_path(domain):
     # Remove 'www.' prefix if present
    domain = domain.lstrip('www.')

    # Remove the '.com' suffix if present
    domain = re.sub(r'\.com$', '', domain)
    return f"outputs/{domain}"

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Web scraping script.")
    
  
    
    # Add arguments to the parser
    parser.add_argument(
        "--driver-options", 
        type=str, 
        required=True, 
        help="Path to the JSON file containing Chrome driver options."
    )
    parser.add_argument(
        "--base-url", 
        type=str, 
        required=True, 
        help="Base URL of the website to scrape."
    )
    parser.add_argument(
        "--max-scrapers", 
        type=int, 
        required=False, 
        help="Maximum number of concurrent scrapers."
    )
    args = parser.parse_args()

    # Start the Chrome driver with the options from the JSON file
    print("Starting driver......")
    driver = start_driver(driver_options_path=args.driver_options)

    domain = extract_domain(base_url=args.base_url)
    output_path = extract_output_path(domain = domain)
    # Scrape the page
    print("Scraping page...")
    scraping_engine(driver=driver, base_url=args.base_url, domain=domain, output_dir=output_path, max_scrapers=args.max_scrapers)

    # Quit the driver
    print("Quitting.....")
    quit_driver(driver)

if __name__ == '__main__':
    main()