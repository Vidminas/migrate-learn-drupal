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

! DO NOT USE ! At the moment this is not updated to integrate with the Drupal uploader. I may update this in the future, if needed.

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

This project creates Drupal Books for course pages, which have links between each other. All the course book pages are also placed into one course group, which allows managing permissions and adding fields that apply to the whole course.

1. Log in as an administrator (or ask your Drupal administrator to do the steps below)
1. Go to 'Extend' admin tab and enable HTTP Basic Authentication and JSON:API modules
1. Visit `${drupal_url}/admin/config/services/jsonapi` and enable JSON:API create, read, update, and delete operations
1. Install, enable, and configure the [GraphQL Book](https://www.drupal.org/project/graphql_book) Drupal module (follow module documentation)
1. Install, enable, and configure the Group Drupal module:
   1. Go to Administration > Groups > Group types and press "+ Add group type". In the name field, enter "Course" (or, if you want to set it to something else, it's possible but you will need to update the machine names and API routes in the configuration code). Leave group settings and creator settings with defaults, but in access settings, tick "Automatically configure useful default roles", "Automatically configure an administrative role", "Automatically assign this administrative role to group creators". Save the group type
   1. Click 'manage fields' for the new group type and "+ Add field". Set the field type to "Text (plain)" and label to "Acronym" (same rules as with group type name apply). Continue leaving the rest to default values and save the new field
   1. Navigate to the 'content' settings for the Course group type and install the "Group node (Book page)" plugin. Set group cardinality to 1 (and the content cardinality setting should be fixed at 1 already). Do not tick the use 2-step wizard box. Confirm with the "Install plugin" button
   1. With Drupal 10.0.9 + Group 3.1.0 module, creating group relationships fails with HTTP 500 error:
   
   ```
   Drupal\\group\\Plugin\\Group\\RelationHandler\\EmptyAccessControl::relationshipCreateAccess(): Argument #1 ($group) must be of type Drupal\\group\\Entity\\GroupInterface, null given, called in drupal\\modules\\contrib\\group\\src\\Entity\\Access\\GroupRelationshipAccessControlHandler.php on line 61
   ```
   This is a known bug: https://www.drupal.org/project/group/issues/2872645. It can be resolved by applying patch until official fix is released. Instructions for applying patches can be found here: https://www.drupal.org/docs/develop/git/using-git-to-contribute-to-drupal/working-with-patches/applying-a-patch-in-a-feature-branch. Add to `composer.json > extra`:
   ```
   "patches": {
      "drupal/group": {
         "#2872645 - Creating Group content via JSON:API": "https://www.drupal.org/files/issues/2023-02-15/group-add-content-2872645-50.patch"
      }
   }
   ```

   If this fails to apply the patch for some reason, you can also download the patch to the group module directory and apply it manually using `patch -p 1 -i ${patch_filename}`

1. In the `.env` file:
   1. Replace the `DRUPAL_BASE_URL` value with the link to your Drupal instance
   1. Replace the `DRUPAL_GRAPHQL_URL` value if using a different graphql endpoint
   1. Replace the `DRUPAL_JSONAPI_URL` value if using a different JSON:API endpoint
   1. Replace the `DRUPAL_COURSE_ID` value with the course identifier (in the previous steps, a json file named as `<course id>.json` will be created in the directory defined by `COURSE_DATA_DIR`)
   1. Replace the `DRUPAL_COURSE_ACRONYM` value with a prefix to be used in all created page titles
   1. Replace the `DRUPAL_USERNAME` and `DRUPAL_PASSWORD` values with account details of an account with permission to execute GraphQL and JSON:API requests

1. Open `upload_drupal.ipynb` and run all the cells


## Useful commands and links

Blackboard Learn API documentation: <https://developer.blackboard.com/portal/displayApi>

Drupal GraphQL documentation: <https://drupal-graphql.gitbook.io/graphql/>

If using Docker Compose to run Drupal (I use <https://hub.docker.com/r/bitnami/drupal-nginx>), then you can use `docker exec -it drupal_drupal_1 bash` to get an interactive shell in the Docker image.

And for Docker Compose with a local Dockerfile to run additional setup commands, use `docker compose up --build --force-recreate --no-deps` to force rebuild the image, when Docker doesn't pick up on Dockerfile changes.

Drupal modules can be enabled from the command line using drush: `drush pm:enable -y graphql`.
