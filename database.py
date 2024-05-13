import pymongo

MONGODB_HOST = 'mongodb+srv://<user>:<password>@cluster0.vkv0htm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
def read_configuration_file():
    with open('db_config.txt') as f:
        lines = f.readlines()
        db_config = {}
        for line in lines:
            key, value = line.split(':')
            db_config[key] = value.strip()
    return db_config

def connect(host = MONGODB_HOST):
    db_config = read_configuration_file()
    user = db_config['user']
    password = db_config['password']
    client = pymongo.MongoClient(host.replace('<password>', password).replace('<user>', user))
    db = client['Decathlon']
    return db

def get_collection(collection_name):
    db = connect()
    return db[collection_name]


def insert_into_db(collection_name, data: dict):
    collection = get_collection(collection_name)
    collection.insert_one(data)
    return True