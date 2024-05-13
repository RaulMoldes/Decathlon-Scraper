import pymongo


def read_configuration_file():
    with open('db_config.txt') as f:
        lines = f.readlines()
        db_config = {}
        for line in lines:
            key, value = line.split(':')
            db_config[key] = value.strip()
    return db_config

def connect():
    db_config = read_configuration_file()
    user = db_config['user']
    password = db_config['password']
    host = db_config['connection']
    client = pymongo.MongoClient(host.replace('<password>', password).replace('<user>', user))
    db = client['Decathlon']
    return db