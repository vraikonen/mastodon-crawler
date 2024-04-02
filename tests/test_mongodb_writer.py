import pytest
from datetime import datetime, timedelta, timezone
from pymongo import MongoClient

from modules.api_requests import fetch_toots
from utils.reading_config import reading_config_db_params
from utils.intialize_user import initialize_users
from utils.mongodb_writer import write_data

def test_mongo_db_writer():
    config_database = "config/config-db-params.ini"
    (server_path, database, collection, max_id, min_id) = reading_config_db_params(
        config_database
    )

    client = MongoClient(server_path)
    db = client[database]
    # let's define new collection
    collection = db["test_mongodb_writer"]
    
    # Define at least min_id
    min_id = (2021, 7, 10, 0, 0, 0) 
    
    # Create datetime objects and adjust for time zone
    min_id_datetime = datetime(*min_id)

    mastodons = initialize_users()
    
    # Fetch toots, write it, read it again and assert
    result = fetch_toots(mastodons[0], limit=40, max_id=None, min_id=min_id_datetime)
    write_data(result, collection)
    
    id_list = [item["id"] for item in result]
    cursor = collection.find()
    id_list_db = [doc.get("id") for doc in cursor]

    assert id_list == id_list_db
        
    # Delete collection
    db.drop_collection(collection)
