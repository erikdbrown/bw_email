## System Requirements
- Python 3
- Pip
- SQLite

## Dependency Installation
```
pip install -r requirements.txt
path/to/python3 manage.py migrate
```

## Run Server
`path/to/python3 manage.py runserver`

Local server will be accessible at `http://127.0.0.1:8000/`

## Run Tests
`path/to/python3 manage.py test`

## Settings:

In `brightwheel/settings.py`, the following settings can be set. These can also be set within your local environment:
- `EMAIL_PROVIDER`: `'spendgrid'` or `'snailgun'`. This determines which is the default provider for the environment
- `SPENDGRID_KEY`: Spendgrid API Key
- `SNAILGUN_KEY`: Snailgun API Key

```
EMAIL_PROVIDER = os.environ.get('EMAIL_PROVIDER', 'spendgrid')
SPENDGRID_KEY = os.environ.get('SPENDGRID_KEY', <API_KEY_GOES_HERE>)
SNAILGUN_KEY = os.environ.get('SNAILGUN_KEY', <API_KEY_GOES_HERE>)
```

## Homework Questions

### Which language, framework and libraries you chose and why
I chose Python and Django for this project because these were the easiest to set up a quick environment without needing to write a bunch of boilerplate code. 

Most of the work related to this assignment are in:
- `email_server/views.py`
- `email_server/models.py`
- `email_server/services.py`
- `email_server/tests.py`

I also added the `requests` dependency because it's an easy interface for the native Python `http` modules.

### Tradeoffs you might have made, anything you left out, or what you might do differently if you were to spend additional time on the project
One trade off I made was in parsing the HTML body of the email into plain text. Since the Spendgrid and Snailgun APIs do not require or consume this data, I decided to skip it because it did not seem like a P1 to achieve an MVP.

For the `SnailgunProvider`, I did not have time to write code that will periodically check that queued emails are, in fact, being sent. I'd take some time to think about interfacing `GET` requests to their `/emails` API. This way the code will have a way to evaluate if there is a problem.

Though I included some tests, I didn't have time to include tests for the interface of this app and the snailgun and spendgrind APIs. The validation and error handling with this interface is fairly minimal, so I'd like to go back and beef that up.

### Anything else you wish to include.
Also, it looks like the api keys in the documentation are the same for both email providers. I was able to use the token to interface with Snailgun, but the same token was not valid for Spendgrid.
