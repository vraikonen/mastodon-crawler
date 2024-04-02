import logging
from retrying import retry

from utils.mongodb_writer import write_data
from modules.mongodb_query import get_last_toot_id


@retry(wait_fixed=60000)  # Retry every minute foreeeeveeer
def fetch_toots(mastodon, limit=40, max_id=None, min_id=None, since_id=None):
    try:
        # Call the API to get the toots
        results = mastodon.timeline_public(
            limit=limit, max_id=max_id, min_id=min_id, since_id=since_id
        )
    except Exception as e:
        logging.info(
            f"An error occurred with the request: {str(e)}. If error of a TypeError, ignore."
        )

    return results


def get_history(mastodons, collection, max_id, min_id):

    # Check if the script was run before
    try:
        max_id = get_last_toot_id()
    except Exception as e:
        logging.info(f"Error for get_last_toot_id(): {e}")
        max_id = max_id

    # Find ID coressponding to the start_date of your crawling period
    result = fetch_toots(mastodons[0], limit=1, max_id=None, min_id=min_id)
    min_id = result[0]["id"]

    # Initialize number of processed batches
    processed_batches = 0
    while True:
        # Get toots
        for mastodon in mastodons:
            while True:

                # Fetch toots, we start with max_id(end date) and go backwards
                results = fetch_toots(mastodon, max_id=max_id, min_id=None)

                # Get some details, max_id is used for pagination
                max_id = results[-1]["id"]
                time_stamp = results[-1]["created_at"]
                processed_batches += 1

                # Results to list of dictionaries - needed for MongoDB
                results_list = [dict(item) for item in results]
                write_data(results_list, collection)
                logging.info(
                    f"Last toot ID: {min_id}; Last toot timestamp: {time_stamp}"
                )

                # Initiate new mastodon if the current one submitted 100 requests
                if processed_batches >= 100:
                    processed_batches = 0
                    break

            # Break the loop if we have reached the last toot we want
            if int(min_id) >= int(results[-1]["id"]):
                break

        # Break the loop if we have reached the last toot we want
        if int(min_id) >= int(results[-1]["id"]):
            logging.info("We have reached our start date. Script is terminated.")
            break


def get_present():
    pass
