# migrate-learn-drupal

Migration tool for moving content from Blackboard Learn to Drupal using their REST APIs

## Setup instructions

1. Clone this repository
1. Install Python (at least v3.8 is required)
1. Run `pip install -r requirements.txt` in the project directory
1. Copy `.env.sample` to a new `.env` file and fill in all the fields that you can (see instructions below for obtaining the remaining data)

## Blackboard Learn instructions

This project contains two modes of working with Blackboard Learn: 1) using the API to download course data or 2) using exported course archives locally.

### Using the Learn API

1. In the `.env` file, replace the `LEARN_BASE_URL` value with the link to your Blackboard Learn instance
1. Create Blackboard Developer account at <https://developer.blackboard.com/>
1. Create a new Blackboard API application and copy the application key (that's the client ID) and secret (that's the client secret) into the `.env` file
1. Login as an administrator (or ask your Blackboard Learn administrator to do the steps below)
1. Register the Blackboard API application in the Blackboard Learn instance (see <https://help.blackboard.com/Learn/Administrator/Hosting/System_Integration/Compare_Building_Blocks_and_Rest> for instructions)
1. Choose a course you would like to download data from Blackboard Learn for. Copy its course ID (it appears as a grey string above each course name in the course list in the web UI) into `.env`
1. Open `download_learn.ipynb` and run all the cells; watch out for any errors -- if there are any, resolve them before continuing and re-run the cells. This should create a JSON file with all the course content

### Using exported Learn course archives locally

1. Export a course using the Learn web interface. This project relies on several assumptions: the exported course ID must begin with 'INFR`, exported content must contain 'Welcome' and 'Course Information' content areas, and 'Navigation Settings' must be included
1. Download and copy the course export file into the project directory
1. In the `.env` file:
   1. Replace the `LEARN_EXPORT_FILE` field with the zip filename
   1. If you would like, you can change the directory where the content will be unzipped by modifying the `COURSE_DATA_DIR` value
1. Open `extract_learn.ipynb` and run all the cells; watch out for any errors -- if there are any, resolve them before continuing and re-run the cells. This should create a JSON file with all the course content

## Drupal instructions

This project contains two modes of working with Drupal: 1) uploading course pages as Group nodes or 2) uploading course pages as Book nodes. At the moment 1) only works with Learn API downloaded data and 2) only works with course export file data.

### Using Drupal Group

1. Install, enable, and configure the Group Drupal module (this can be quite extensive and steps are subject to change, instructions to be added if needed)
1. In the `.env` file, replace the `DRUPAL_BASE_URL` value with the link to your Drupal instance
1. Log in as an administrator (or ask your Drupal administrator to do the steps below)
1. Go to 'Extend' admin tab and enable HTTP Basic Authentication and JSON:API modules
1. Visit `${drupal_url}/admin/config/services/jsonapi` and enable JSON:API create, read, update, and delete operations
1. Copy administrator account username and password into the `.env` file
1. If you haven't done this already in the steps for using the Learn API above, choose a course you would like to migrate from Blackboard Learn to Drupal and copy its course ID into `.env` (if using the course archive mode, then a json file named as `<course id>.json` will be created in the directory defined by `COURSE_DATA_DIR`).
1. Open `upload_drupal_group.ipynb` and run all the cells

### Using Drupal Book

1. Install, enable, and configure the [GraphQL Book](https://www.drupal.org/project/graphql_book) Drupal module (follow module documentation)
1. In the `.env` file:
   1. Replace the `DRUPAL_BASE_URL` value with the link to your Drupal instance
   1. Replace the `DRUPAL_GRAPHQL_URL` value if using a different graphql endpoint
   1. Replace the `DRUPAL_COURSE_ID` value with the course identifier (can be found from the created JSON filename)
   1. Replace the `DRUPAL_COURSE_ACRONYM` value with a prefix to be used in all created page titles
   1. Replace the `DRUPAL_USERNAME` and `DRUPAL_PASSWORD` values with account details of an account with permission to execute GraphQL requests
1. Open `upload_drupal_book.ipynb` and run all the cells

## Useful commands and links

Blackboard Learn API documentation: <https://developer.blackboard.com/portal/displayApi>

Drupal GraphQL documentation: <https://drupal-graphql.gitbook.io/graphql/>

If using Docker Compose to run Drupal (I use <https://hub.docker.com/r/bitnami/drupal-nginx>), then you can use `docker exec -it drupal_drupal_1 bash` to get an interactive shell in the Docker image.

And for Docker Compose with a local Dockerfile to run additional setup commands, use `docker compose up --build --force-recreate --no-deps` to force rebuild the image, when Docker doesn't pick up on Dockerfile changes.

Drupal modules can be enabled from the command line using drush: `drush pm:enable -y graphql`.

TODO: Restrict GraphQL access with basic auth? https://drupal.stackexchange.com/questions/297350/how-do-i-restrict-graphql-access-with-basic-auth
