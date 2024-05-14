from database import connect
from utils.utils import get_valid_queries, get_data
import pandas as pd
from data_visualization.figures import plot_characteristics_rating
import sys
import argparse
import unidecode

db = connect()

valid_queries = get_valid_queries()


products = get_data(db,'Product_Data')
reviews = get_data(db, 'Product_Reviews')
characteristics = get_data(db, 'Product_Characteristics')


def set_characteristics_rating(row):
    product_id = row['product_id']
    rating = reviews[reviews['product_id'] == product_id]['rating']
    if len(rating) == 0:
        return None
    return rating.mean()

def visualize_characteristics_rating(query = 'balón'):
    global characteristics
    characteristics = characteristics[characteristics['query'] == unidecode.unidecode(query)]
    characteristics['rating'] = characteristics.apply(set_characteristics_rating, axis=1)
    plot_characteristics_rating(characteristics,)
    
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data Exploitation Arguments')
    parser.add_argument('--query', type=str, help='Query to filter the data',required=True)
    args = parser.parse_args()
    visualize_characteristics_rating(query= args.query)
    sys.exit(0)