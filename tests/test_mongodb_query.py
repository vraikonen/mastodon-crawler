from pymongo import MongoClient
from utils.reading_config import reading_config_db_params
from modules.mongodb_query import get_last_toot_id


from unittest.mock import MagicMock


def test_get_last_toot_id():

    # Go to your db from config file and find the "oldest" scraped tooth
    oldest_toot_id = 106589544834980076
    last_tooth = get_last_toot_id()
    assert oldest_toot_id == last_tooth
