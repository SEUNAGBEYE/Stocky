## Stocky
APIs for a stock broking firm that allows them to upload daily stock prices, and send notifications to their users once new stocks are uploaded or existing stocks are updated.

#### Features
- Admin section to upload stocks
- When uploading stocks, a CSV file must be present with the following fields stock name, opening price, closing price, the highest price of the day, the lowest price of the day, number of shares in the company
- Once a stock has been uploaded or updated, notifications should be scheduled to be sent to the users twice (morning & evening) that day
- Authentication should be token based
- Users should be able to request for all stocks of the day

#### Technologies Used
- Python 3.7
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
          celery -A main --loglevel=info
        ```
   
##  Running Celery beat
  - After setting up the Celery worker, you need to start the `celery-beat` used to to trigger `celery` scheduled tasks
  
  - In a new terminal tab start `celery-beat` with:
   
    ```
      celery -A main beat -l INFO
    ```

#### Application Url
Coming soon!