import sys

from utils.reading_config import reading_config_db_params
from utils.logging import logging_crawler, custom_exception_hook

from utils.mongodb_writer import initialize_mongodb
from utils.intialize_user import initialize_users
from utils.mongodb_writer import create_index

from modules.api_requests import get_history

## TODO Log response.header, track
if __name__ == "__main__":
    # Initiate logging, set the custom exception hook
    logging_crawler()
    sys.excepthook = custom_exception_hook

    # Read database and script config
    config_database = "config/config-db-params.ini"
    (
        server_path,
        database,
        collection,
        max_id,
        min_id,
    ) = reading_config_db_params(config_database)

    # Connect to database and create database and collections
    (toots_collection) = initialize_mongodb(server_path, database, collection)

    # Create an index on the id field
    create_index(toots_collection, "id")

    # Initialize users
    mastodons = initialize_users()

    # Start crawling
    get_history(mastodons, toots_collection, max_id, min_id)
