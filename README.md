<a name="readme-top"></a>


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://git.sbg.ac.at/geo-social-analytics/geo-social-media/mastodon-crawler">
    <img src="img/mastodon.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Mastodon Crawler</h3>

  <p align="center">
    This Python script fetches historical toots(statutes) from public Mastodon federations (instances). Restricted or private toot cannot be accessed. User defines crawling period by providing start and end date as GMT+0. Toots are stored in MongoDB.
    <br />
    <a href="https://git.sbg.ac.at/geo-social-analytics/geo-social-media/mastodon-crawler"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://git.sbg.ac.at/geo-social-analytics/geo-social-media/mastodon-crawler">View Demo</a>
    ·
    <a href="https://git.sbg.ac.at/geo-social-analytics/geo-social-media/mastodon-crawler/-/issues">Report Bug</a>
    ·
    <a href="https://git.sbg.ac.at/geo-social-analytics/geo-social-media/mastodon-crawler/-/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
	<li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#obtaining-credentials-for-telegram-api">Obtaining Credentials for Telegram API</a></li>
	<li><a href="#database-configuration">Database configuration</a></li>
      </ul>
    </li>
    <li>
	<a href="#code-explanation">Code Explanation</a>
    	<ul>
         <li><a href="#general-overview">General Overview</a></li>
         <li><a href="#flowchart">Flowchart</a></li>
	       <li><a href="#restart-logic">Restart logic</a></li>
         <li><a href="#network/iteration-logic">Network/Iteration logic</a></li>
         <li><a href="#multi-client-and-ratelimit-logic">Multi-client and ratelimit logic</a></li>
	</ul>
    </li>
    <li><a href="#db-data-structure">DB Data Structure</a></li>
    <li><a href="#queries-example-and-tips">Queries example and tips</a></li>
    <li><a href="#Suggestions-and-Issues">Suggestions and Issues</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites
* Python (latest stable release)
* MongoDB Community Server (latest stable release)
* Mastodon.py (latest stable release)
* PyMongo (latest stable release)

### Step 1: 

1. Clone the repo.

2. Create a Python environment.

3. Install `requirements.txt`.
```
pip install -r requirements.txt
```

### Step 2: Obtaining Credentials for Mastodon API


1. Create and verify a mastodon account, preferably on mastodon.social instance.

2. Remember email and password of your mastodon account.

3. You need to fill the config file with email, password and instace URL. Refer to the example user config file in the `config/user-example` folder under the name `config-user-example.ini`. 

4. You can change the names of the folder and file, but the path to the folder needs to start with `config/user`, and config file needs to start with `config-user`. This means that string `-example` that is at the end of both is still valid name.

5. In the config file `config-user-example.ini`, there are two variables `client_token_path` and `user_token_path`. You can see that both strings start with `config/user-example`, thus it points to the folder where the config file is located. If you change the name of the folder, you need to update both variables, so that it still points out to the user's folder.

### Additional (strongly suggested) Step: Utilize more accounts

1. If you want to have more accounts (and I do suggest, maybe 5, as the script is optimized to work with more than 1), please follow mentioned rules in regards to naming and have different name for each of the folders containing user configuration file.

2. Let's assume we have three user accounts. In that case our `config` folder could be organized as follows:

        
        config/
        ├── user1/
        │   └── config-user.ini
        ├── user2/
        │   └── config-user.ini
        ├── user3/
        │   └── config-user.ini
        └── config-db-params.ini
        
3. You can see that we start the name of our user folders with the string `user` and they all differ between each other. We can also see that the name of the config file inside the user folder starts with `config-user`. Finally: **do not forget to change the variables `client_token_path` and `user_token_path` inside each of the config files**. For example, in the case of `user1`, the setup is: 

        client_token_path = config/user1/pytooter_clientcred.secret
        user_token_path = config/user1/pytooter_usercred.secret

### Step 3: Database configuration

#### Option 1 - Recommended Database configuration with .msi installer
1. Visit the [MongoDB download page](https://www.mongodb.com/try/download/community) and download Community Server. 

2. The easiest installation is through Windows installer (msi package), by selecting the "Run Service as Network Service user" option when prompted during the installation process.

3. Optionally, change path to the logs and data folders during the installation.

4. Navigate to the `config` folder and modify the `config-db-params.ini` file. Update the `server_path` (default port: 27017, or adjust it in `bin/mongo.cfg` within the MongoDB installation folder) along with the database and collection names.

5. Optionally change the database name and the collection name. Check [naming restrictions for MongoDB](https://www.mongodb.com/docs/manual/reference/limits/?_ga=2.67582801.1990405345.1706732504-2064098827.1705526269#naming-restrictions).

#### Option 2: Alternative Database configuration with MongoDB binaries (Windows)
Since the Windows .msi distribution needs be installed on the system drive, here are the steps for installing MongoDB binaries which can be installed on the data disk.

1. Visit the [MongoDB download page](https://www.mongodb.com/try/download/community) and choose MongoDB binaries (zip package).

2. Extract the downloaded archive to a location of your choice.

3. Create the following folders at the location of your choice and use them in the next step: 
  - `log` for logging performance of the database and 
  - `data` to store actual data.

4. Launch the command prompt with **administrator privileges**, navigate to the `bin` folder in the directory of extracted MongoDB binaries, and run the following commands to create Windows Service (adjust the paths to `log` and `data` according to your system location):
    ```bash
    mongod --repair 

    mongod --remove 

    mongod --bind_ip  127.0.0.1  --logpath  E:/MongoDBbin/log/mongod.log  --logappend  --dbpath  E:/MongoDBbin/data/db  --port 27017 --serviceName "MongoDB-bin" --serviceDisplayName "MongoDB-bin" --install

    net start MongoDB-b
    ```

5. Check [MongoDB configuration options](https://www.mongodb.com/docs/manual/reference/configuration-options/) to understand the arguments. 

6. Now you can adjust MongoDB service preferences through the Windows Services application.

    > **Note:** This set up of MongoDB binaries excludes an option to configure the port to the server and the path to the data directory in the file `bin/mongo.cfg`, as all configurations have been set through the preceding commands.

7. To finish setting up MongoDB, follow the steps 5 and 6 outlined in the earlier section "Database Configuration (Windows .msi)". 

### Step 4: Run the script 

1. Open the file `config/config-db-params.ini` and define start and end date of desired crawling period. S

4. Run the `main.py` script.
    ```
    python main.py
    ```

### Restart of the script
If terminated, script will continue where it stopped as it reads the last processed ID from the database. This means, if you want to start a new crawling process, change the Database configuration to store the data in the new database/collection. 

<!-- Queries example and tips -->
## Queries example and tips
Check notebooks with the examples on how to query data retrieved from Mastodon <a href="https://git.sbg.ac.at/geo-social-analytics/geo-social-media/telegram-crawler/-/tree/main/notebooks">here</a> (on gitlab) or [here](./notebooks) (if you cloned the repository to your local machine).


<!-- Suggestions and Issues -->
## Feature Requests and Bug Reports

See the [open issues](https://git.sbg.ac.at/geo-social-analytics/geo-social-media/telegram-crawler/-/issues) for a full list of proposed features (and known issues).

    Currently, there could be a nicer date-time configuration and not ID, as well as user network. Notebook with the code that retrieves and print user network is in notebooks/mastodon-network.ipynb

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []() Nefta
* []() David

<p align="right">(<a href="#readme-top">back to top</a>)</p>
