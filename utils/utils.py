from database import get_collection
import pandas as pd

def get_valid_queries():
    with open('queries.txt', 'r') as file:
        queries = file.readlines()
    return [query.strip() for query in queries]

def get_data(db, collection_name: str = 'Product_Data'):
    collection = get_collection(db, collection_name=collection_name)
    data = collection.find()
    return pd.DataFrame(data)

