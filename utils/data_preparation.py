import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler


PRODUCT_DATA = 'data/decathlon_products.csv'
CHARACTERISTICS_DATA = 'data/decathlon_characteristics.csv'


def get_discount_magintude(row):
    if row['discount']:
        return abs(row['price'] - row['previous_price'])
    else:
        return 0


def encode_categorical_data(data, columns):
    for column in columns:
        data[column+'_encoded'] = LabelEncoder().fit_transform(data[column])
        data = data.drop(column, axis=1)
    return data


def set_index(data, index='product_id'):
    if index not in data.columns and 'id' in data.columns:
        data[index] = data['id']
    return data.set_index(index).astype('str')


def pivot_data(data, index, columns):
    data = data[[index, columns]]
    data = data.groupby(index).value_counts().reset_index()
    return data.pivot(index=index, columns=columns, values='count').fillna(0)


def preprocess_product_data(filepath: str = PRODUCT_DATA):
    product_data = pd.read_csv(filepath)
    product_data = encode_categorical_data(product_data, ['brand', 'genre'])
    product_data['rating'] = product_data['rating'].fillna(0)
    product_data['discount_magnitude'] = product_data.apply(
        get_discount_magintude, axis=1)
    product_data = set_index(product_data)
    product_data = product_data.drop(
        ['name', 'sticker', 'discount', 'color', 'description', 'previous_price', '_id', 'id'],  axis=1)
    return product_data


def preprocess_characteristics_data(filepath: str = CHARACTERISTICS_DATA):
    characteristics_data = pd.read_csv(filepath)
    characteristics_data['product_id'] = characteristics_data['product_id'].astype(
        'str')
    characteristics_data = pivot_data(
        characteristics_data, 'product_id', 'title')
    return characteristics_data


def join_data(product_data, characteristics_data, on='product_id'):
    joined_data = product_data.join(characteristics_data, how='inner', on=on)
    return joined_data
