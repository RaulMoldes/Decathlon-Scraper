from src.scraper.driver import start_chrome_driver, quit_driver
from src.scraper.scrape_page import scrape_page
import argparse

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Web scraping script.")
    
    # Add arguments to the parser
    parser.add_argument(
        "--driver_options", 
        type=str, 
        required=True, 
        help="Path to the JSON file containing Chrome driver options."
    )
    parser.add_argument(
        "--base_url", 
        type=str, 
        required=True, 
        help="Base URL of the website to scrape."
    )
    parser.add_argument(
        "--domain", 
        type=str, 
        required=True, 
        help="Domain of the website to scrape (e.g., www.example.com)."
    )
    parser.add_argument(
        "--output_path", 
        type=str, 
        required=True, 
        help="Directory path where the output data will be saved."
    )

    # Parse the arguments
    args = parser.parse_args()

    # Start the Chrome driver with the options from the JSON file
    print("Starting chrome driver......")
    driver = start_chrome_driver(driver_options_path=args.driver_options)

    # Scrape the page
    print("Scraping page...")
    scrape_page(driver=driver, base_url=args.base_url, domain=args.domain, output_dir=args.output_path)

    # Quit the driver
    print("Quitting.....")
    quit_driver(driver)

if __name__ == '__main__':
    main()