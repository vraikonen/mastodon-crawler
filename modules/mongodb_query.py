from pymongo import MongoClient
from utils.reading_config import reading_config_db_params

def get_last_tooth_id():
    
    # Connect to db 
    config_database = "config/config-db-params.ini"
    (
        server_path,
        database,
        collection,
        max_id,
        min_id
    ) = reading_config_db_params(config_database)

    client = MongoClient(server_path)
    db = client[database]
    collection = db[collection]
    
    # Define the sort condition to get the oldest tooth
    sort_condition = [('id', 1)]
    first_document = collection.find_one(sort=sort_condition)
    
    return first_document["id"]