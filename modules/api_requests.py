import logging 
from retrying import retry

from utils.mongodb_writer import write_data
from modules.mongodb_query import get_last_tooth_id
import time

@retry(wait_fixed=60000) # Retry every minute foreeeeveeer
def fetch_toots(mastodon, max_id=None, min_id=None, since_id=None):
    try:
        # Call the API to get the toots
        results = mastodon.timeline_public(
            limit=40,
            max_id=max_id,
            min_id=min_id,
            since_id=since_id
        )
    except Exception as e:
        logging.info(f"An error occurred with the request: {e}")

    return results

def get_history(mastodons, collection, max_id, min_id):
    
    # Check if the script was run before
    try:
        max_id = get_last_tooth_id()
    except Exception as e:
        logging.info(f"Error for get_last_tooth_id(): {e}")
        max_id = int(max_id)
    
    
    # Initialize number of processed batches
    processed_batches = 0
    start_time = time.time()
    while True:
        # Get toots
        for mastodon in mastodons:
            while True:
                results = fetch_toots(mastodon,max_id=max_id)
                # Get some info for print and log file
                max_id = results[-1]['id']
                time_stamp = results[-1]["created_at"]
                processed_batches += 1
                
                # Results to list of dictionaries - needed for MongoDB
                results_list = [dict(item) for item in results]
                write_data(results_list, collection)
                
                # Check time
                end_time = time.time()
                elapsed_time = end_time - start_time

                print(f"Timestamp of the last tooth from the current batch: {time_stamp}")
                print(f"Number of batches processed in this run (40 toots per batch): {processed_batches}")
                logging.info(f"Last tooth ID: {max_id}; Last tooth timestamp: {time_stamp}")
                print(f"Elapsed time:{elapsed_time}")
                print(50*"==")
                
                if processed_batches >= 100:
                    processed_batches = 0
                    break


        
        # Break the loop if we reached last tooth we want
        if int(min_id) >= results[-1]["id"]:
            break
        
def get_present():
    pass
