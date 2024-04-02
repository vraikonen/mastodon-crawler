import configparser
from datetime import datetime, timedelta


def reading_config_user(config_file):
    """
    Reads configuration values from a Mastodon user config file.

    Returns:
    tuple: A tuple containing the following configuration values:
        - api_base_url (str): The Mastodon instance URL.
        - client_token_path (str): Path to the file for storing application credential.
        - user_token_path (str): Path to the file for storing user credentials.
        - user_email (str): The user's email for authentication.
        - user_pass (str): The user's password for authentication.
    """
    # Reading Configs
    config = configparser.ConfigParser()
    config.read(config_file)
    # Base URL of the Mastodon instance
    api_base_url = config["Mastodon"]["api_base_url"]
    client_token_path = config["Mastodon"]["client_token_path"]
    user_token_path = config["Mastodon"]["user_token_path"]
    user_email = config["Mastodon"]["user_email"]
    user_pass = config["Mastodon"]["user_pass"]

    return api_base_url, client_token_path, user_token_path, user_email, user_pass


def reading_config_db_params(config_file):
    """
    Reads database configuration values from a database config file and two script related variables.

    Parameters:
        config_file (str): The path to the database config file.

    Returns:
        tuple: A tuple containing the following configuration values:
            - server_path (str): The server path for the database.
            - database (str): The name of the database.
            - collection (str): Name of the collection that stores toots.
            - max_id (datetime): The maximum ID value for toots as datatime object.
            - min_id (datetime): The minimum ID value for toots as datetime object.
    """
    # Reading Configs
    config = configparser.ConfigParser()
    config.read(config_file)

    # Setting configuration values
    server_path = config["Database"]["server_path"]

    database = config["Database"]["database"]

    collection = config["Database"]["collection"]

    max_id = config["Database"]["max_id"]

    min_id = config["Database"]["min_id"]

    # Create datetime object to be returned by the function
    max_id = datetime.strptime(max_id, "%Y, %m, %d, %H, %M, %S")
    min_id = datetime.strptime(min_id, "%Y, %m, %d, %H, %M, %S")
    # Add one hour, Mastodon somehow returns one hour less from what is provided
    max_id += timedelta(hours=1)
    min_id += timedelta(hours=1)

    return (
        server_path,
        database,
        collection,
        max_id,
        min_id,
    )
