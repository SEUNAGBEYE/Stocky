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

#### Application Url
Coming soon!