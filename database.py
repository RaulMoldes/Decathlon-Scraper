import pymongo
import unidecode
MONGODB_HOST = 'mongodb+srv://<user>:<password>@cluster0.vkv0htm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'


def read_configuration_file():
    with open('db_config.txt') as f:
        lines = f.readlines()
        db_config = {}
        for line in lines:
            key, value = line.split(':')
            db_config[key] = value.strip()
    return db_config


def connect(host=MONGODB_HOST):
    db_config = read_configuration_file()
    user = db_config['user']

    password = db_config['password']

    print("Connecting to database...")
    print("HOST:")
    print(host.replace('<password>', password).replace('<user>', user))
    client = pymongo.MongoClient(host.replace(
        '<password>', password).replace('<user>', user))
    db = client['Decathlon']
    return db


def get_collection(db, collection_name):
    return db[collection_name]


def insert_into_db(db, collection_name, data: dict):
    collection = get_collection(db, collection_name)
    if collection_name in ["Products", "Product_Data"]:
        intent = collection.find_one({"id": data["id"]})
    else:
        intent = collection.find_one({"title": data["title"],"product_id": data["product_id"]})
    if intent:
        print("Data already exists in database")
        return False

    try:
        collection.insert_one(data)
    except Exception as e:
        print(e)
        print("Error inserting data into database, saving to file instead.")
        return False
    return True


def read_collection(db, collection_name):
    collection = get_collection(db, collection_name)
    return collection.find()


def read_collection_by_query(db, collection_name, query):
    collection = get_collection(db, collection_name)
    return collection.find(query)


def update_all_items(db, collection_name, query, data):
    collection = get_collection(db, collection_name)
    return collection.update_many({}, {"$set": data})


data = {"query": unidecode.unidecode("balón")}
db = connect()
for collection in ["Products", "Product_Data", "Product_Reviews", "Product_Characteristics"]:
    update_all_items(db, collection, {"query": unidecode.unidecode("balón")}, data)