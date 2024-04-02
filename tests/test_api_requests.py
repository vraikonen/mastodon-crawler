import pytest
from datetime import datetime, timedelta, timezone

from modules.api_requests import fetch_toots
from utils.intialize_user import initialize_users
from utils.mongodb_writer import write_data

def test_fetch_toots1():
    # Define min and max id based on date and time
 
    min_id = (2021, 7, 10, 0, 0, 0) 
    max_id = (2021, 7, 11, 0, 0, 0)
    
    # Create datetime objects and adjust for time zone
    min_id_datetime = datetime(*min_id)
    max_id_datetime = datetime(*max_id)
    
    # Add one hour, Mastodon somehow returns one hour less from what is provided
    min_id_datetime += timedelta(hours=2)
    max_id_datetime += timedelta(hours=2)
    # Convert min_id_datetime and max_id_datetime to UTC timezone
    min_id_datetime_utc = min_id_datetime.astimezone(timezone.utc)
    max_id_datetime_utc = max_id_datetime.astimezone(timezone.utc)

    mastodons = initialize_users()
    
    # Fetch toots within the specified time range
    result = fetch_toots(mastodons[0], limit=40, max_id=None, min_id=min_id_datetime)
    
    # Check each fetched toot's timestamp falls within the specified range
    for res in result:
        timestamp = res["created_at"]
        print(timestamp)
        # Convert res["created_at"] to a timezone-aware datetime object (assuming it's in UTC)
        timestamp_utc = timestamp.astimezone(timezone.utc)
        assert min_id_datetime_utc <= timestamp_utc <= max_id_datetime_utc, "Toot timestamp not within expected range"


def test_fetch_toots2():
    # Define min and max id based on date and time
 
    min_id = (2021, 7, 10, 0, 0, 0) 
    max_id = (2021, 7, 11, 0, 0, 0)
    
    # Create datetime objects and adjust for time zone
    min_id_datetime = datetime(*min_id)
    max_id_datetime = datetime(*max_id)
    
    # Add one hour, Mastodon somehow returns one hour less from what is provided
    min_id_datetime += timedelta(hours=2)
    max_id_datetime += timedelta(hours=2)
    mastodons = initialize_users()
    
    
    # Send the same request twice
    result1 = fetch_toots(mastodons[0], limit=40, max_id=None, min_id=min_id_datetime)
    result2 = fetch_toots(mastodons[0], limit=40, max_id=None, min_id=min_id_datetime)
    
    # Extract IDs from each result
    ids1 = [res["id"] for res in result1]
    ids2 = [res["id"] for res in result2]
    
    # Check if the IDs from both results match
    assert ids1 == ids2, "IDs from both fetches do not match"

