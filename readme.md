## Stocky
APIs for a stock broking firm that allows them to upload daily stock prices, and send notifications to their users once new stocks are uploaded or existing stocks are updated.

#### Features
- Admin section to upload stocks
- When uploading stocks, a CSV file must be present with the following fields stock name, opening price, closing price, the highest price of the day, the lowest price of the day, number of shares in the company
- Once a stock has been uploaded or updated, notifications should be scheduled to be sent to the users twice (morning & evening) that day
- Authentication should be token based
- Users should be able to request for all stocks of the day

#### Technologies Used
- Python 3.6.5
- Flask
- Flask Restplus
- Sqlalchemy (ORM)
- Reddis (messaging queue)
- Celery (Tasks scheduling/cronjobs)
- Postgres
- Pipenv (Virtual environment)
- Pytest
- AWS (EC2)
- Pivotal Tracker (Project management)

#### Security
This application uses JWT for user authentication and authorization

## Setup 

-   Check that python 3 is installed:

    ```
    python --version
    >> Python 3.6.5
    ```

-   Install pipenv:

    ```
    brew install pipenv or pip install pipenv
    ```

-   Check pipenv is installed:
    ```
    pipenv --version
    >> pipenv, version 2018.6.25
    ```
-   Check that postgres is installed:

    ```
    postgres --version
    >> postgres (PostgreSQL) 10.1
    ```

-   Clone the stocky-api repo and cd into it:

    ```
    git clone https://github.com/SEUNAGBEYE/Stocky.git
    ```

-   Install dependencies:

    ```
    pipenv install
    ```

-   Install dev dependencies to setup development environment:

    ```
    pipenv install --dev
    ```

-   Make a copy of the .env.sample file  and rename it to .env and update the variables

-   Activate a virtual environment:

    ```
    pipenv shell
    ```

-   Apply migrations:

    ```
    flask db upgrade
    ```

-   If you'd like to seed initial data to the database:

    ```
    flask seed
    ```
    to seed everything or
    ```
    flask seed <resource>
    ```
    to seed a specific resource.

    allowed resources arguments are
    ```
    users and stocks
    ```

-   Run the application with either commands:

    ```
    flask run
    ```

- **Running Redis server**
     - Run `bash redis.sh` in the root project directory, this will install redis for you (if not already installed) and also run/start the redis server for the first time on your local machine.
  

##  Running Celery worker

  - Update the `.env` file with the following keys and the appropriate values(`redis_server_url`):
       ```
        CELERY_BROKER_URL=<Your_Redis_Server_URL>
        CELERY_RESULT_BACKEND=<Your_Redis_Server_URL>
      ```


      The update above must be done before you do `flask run`

  
   *Restart **redis/celery***

   - To run redis after it has been stopped run `redis-server`
  
   - In a new terminal tab run the Celery Message Worker with:
   
        ```
          celery -A main worker --loglevel=info
        ```
   
##  Running Celery beat
  - After setting up the Celery worker, you need to start the `celery-beat` used to to trigger `celery` scheduled tasks
  
  - In a new terminal tab start `celery-beat` with:
   
    ```
      celery -A api.tasks.cronjobs beat --loglevel=info
    ```

##  Running tests and generating report

   On command line run: 
   
   ```
   pytest
   ```

   To further view the lines not tested or covered if there is any, 

   An `htmlcov` directory will be created, get the `index.html` file by entering the directory and view it in your browser.

#### Application Url
Coming soon!