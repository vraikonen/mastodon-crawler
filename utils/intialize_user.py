from mastodon import Mastodon
import logging
import glob
import os

from utils.reading_config import reading_config_user


def initialize_user(
    user_folder, api_base_url, client_token_path, user_token_path, user_email, user_pass
):
    """
    Initialize a Mastodon API user instance.

    Args:
        user_folder (str): Path to the user folder.
        api_base_url (str): Base URL of the Mastodon instance.
        client_token_path (str): Path to store the client token.
        user_token_path (str): Path to store the user token.
        user_email (str): User's email for authentication.
        user_pass (str): User's password for authentication.

    Returns:
        mastodon (Mastodon): Initialized Mastodon API user instance.
    """

    # Check if the App is created and if the user is authorized
    if any(glob.glob(os.path.join(user_folder, "*.secret"))):
        # Set up Mastodon API user instance
        try:
            mastodon = Mastodon(api_base_url=api_base_url, access_token=user_token_path)
        except Exception as setup_mastodon_exception:
            logging.error(
                f"Error setting up Mastodon API user instance: {setup_mastodon_exception}"
            )
    # Create App and authorize user
    else:
        # Create a Mastodon application
        try:
            Mastodon.create_app(
                "pytooterapp", api_base_url=api_base_url, to_file=client_token_path
            )
        except Exception as create_app_exception:
            logging.error(
                f"Error creating Mastodon application: {create_app_exception}"
            )

        # Authorize application
        try:
            mastodon = Mastodon(client_id=client_token_path)
            mastodon.log_in(user_email, user_pass, to_file=user_token_path)
        except Exception as log_in_exception:
            logging.error(f"Error logging in to Mastodon: {log_in_exception}")
        # Set up Mastodon API user instance
        try:
            mastodon = Mastodon(api_base_url=api_base_url, access_token=user_token_path)
        except Exception as setup_mastodon_exception:
            logging.error(
                f"Error setting up Mastodon API user instance: {setup_mastodon_exception}"
            )

    return mastodon


import os


def initialize_users():
    """
    Get Mastodon instances from user configuration folders.

    This function searches for user configuration folders within the 'config'
    directory, reads the configuration files named 'config-user' within those
    folders, and initializes Mastodon instances based on the configuration
    data. It returns a list of initialized Mastodon instances.

    Returns:
        list: A list of Mastodon instances.
    """
    mastodons = []
    config_folder = "config"
    # Loop through all folders in the config folder
    for folder_name in os.listdir(config_folder):
        # Check if the folder name starts with "user" and is a directory
        if folder_name.startswith("user") and os.path.isdir(
            os.path.join(config_folder, folder_name)
        ):
            # Construct the path to the user folder
            user_folder = os.path.join(config_folder, folder_name)

            # Loop through all files in the user folder
            for filename in os.listdir(user_folder):
                # Check if the file starts with "config-user"
                if filename.startswith("config-user"):
                    # Process the file
                    file_path = os.path.join(user_folder, filename)

                    # Read configuration and initialize Mastodon instance
                    (
                        api_base_url,
                        client_token_path,
                        user_token_path,
                        user_email,
                        user_pass,
                    ) = reading_config_user(file_path)
                    mastodon = initialize_user(
                        user_folder,
                        api_base_url,
                        client_token_path,
                        user_token_path,
                        user_email,
                        user_pass,
                    )

                    # Append Mastodon instance to the list
                    mastodons.append(mastodon)

    return mastodons
