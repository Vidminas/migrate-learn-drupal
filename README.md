# migrate-learn-drupal
Migration tool for moving content from Blackboard Learn to Drupal using their REST APIs

## Setup instructions
1. Clone this repository
1. Install Python (at least v3.8 is required)
1. Run `pip install -r requirements.txt` in the project directory
1. Copy `.env.sample` to a new `.env` file and fill in all the fields that you can (see instructions below for obtaining the remaining data)

## Blackboard Learn instructions
1. Create Blackboard Developer account at `https://developer.blackboard.com/`
1. Create a new Blackboard API application and copy the application key (that's the client ID) and secret (that's the client secret) into the `.env` file
1. Login as an administrator (or ask your Blackboard Learn administrator to do the steps below)
1. Register the Blackboard API application in the Blackboard Learn instance (see `https://help.blackboard.com/Learn/Administrator/Hosting/System_Integration/Compare_Building_Blocks_and_Rest` for instructions)

## Drupal instructions
1. Log in as an administrator (or ask your Drupal administrator to do the steps below)
1. Go to 'Extend' admin tab and enable HTTP Basic Authentication and JSON:API modules
1. Visit `${drupal_url}/admin/config/services/jsonapi` and enable JSON:API create, read, update, and delete operations
1. Copy administrator account username and password into the `.env` file

## Usage
1. Choose a course you would like to migrate from Blackboard Learn to Drupal. Copy its course ID (it appears as a grey string above each course name in the course list in the web UI) into `.env`
1. Open `download_learn.ipynb` and run all the cells; watch out for any errors -- if there are any, resolve them before continuing and re-run the cells. This should create a JSON file with all the course content
1. Open `upload_drupal.ipynb` and repeat the same