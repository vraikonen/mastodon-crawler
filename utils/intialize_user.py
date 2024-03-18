from mastodon import Mastodon
import logging
import glob
import os

from utils.reading_config import reading_config_user

def initialize_user(user_folder, api_base_url,client_token_path,user_token_path,user_email, user_pass):
    
    # Check if the App is created and if the user is authorized 
    if any(glob.glob(os.path.join(user_folder, '*.secret'))):
        # Set up Mastodon API user instance
        try:
            mastodon = Mastodon(
                api_base_url=api_base_url,
                access_token=user_token_path
            )
        except Exception as setup_mastodon_exception:
            logging.error(f"Error setting up Mastodon API user instance: {setup_mastodon_exception}")
    # Create App and authorize user
    else:
        # Create a Mastodon application
        try:
            Mastodon.create_app(
                'pytooterapp', 
                api_base_url=api_base_url,
                to_file=client_token_path
            )
        except Exception as create_app_exception:
            logging.error(f"Error creating Mastodon application: {create_app_exception}")

        # Authorize application
        try:
            mastodon = Mastodon(client_id=client_token_path)
            mastodon.log_in(
                user_email, 
                user_pass, 
                to_file=user_token_path
            )
        except Exception as log_in_exception:
            logging.error(f"Error logging in to Mastodon: {log_in_exception}")
        # Set up Mastodon API user instance
        try:
            mastodon = Mastodon(
                api_base_url=api_base_url,
                access_token=user_token_path
            )
        except Exception as setup_mastodon_exception:
            logging.error(f"Error setting up Mastodon API user instance: {setup_mastodon_exception}")

    return mastodon


import os

def initialize_users():
    """
    Get Mastodon instances from user configuration folders.

    Returns:
        list: A list of Mastodon instances.
    """
    mastodons = []
    config_folder = 'config'
    # Loop through all folders in the config folder
    for folder_name in os.listdir(config_folder):
        # Check if the folder name starts with "user" and is a directory
        if folder_name.startswith("user") and os.path.isdir(os.path.join(config_folder, folder_name)):
            # Construct the path to the user folder
            user_folder = os.path.join(config_folder, folder_name)

            # Loop through all files in the user folder
            for filename in os.listdir(user_folder):
                # Check if the file starts with "config-user"
                if filename.startswith("config-user"):
                    # Process the file
                    file_path = os.path.join(user_folder, filename)
                    
                    # Read configuration and initialize Mastodon instance
                    api_base_url, client_token_path, user_token_path, user_email, user_pass = reading_config_user(file_path)
                    mastodon = initialize_user(user_folder, api_base_url, client_token_path, user_token_path, user_email, user_pass)
                    
                    # Append Mastodon instance to the list
                    mastodons.append(mastodon)

    return mastodons