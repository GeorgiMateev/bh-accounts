# bh-accounts
Managing financial accounts.
The solution implements two endpoints:
- POST /:customerId/open - to open a new account
- GET /:customerId> - to get account details

You can start the server locally by using docker compose. Chech the testing session below to see how. The server will be available at localhost:5005 for manual testing.

## Setup
Optionally you can create virtual environment to host the project packages:
```
python3 -m venv .venv && source .venv/bin/activate
```

Install packages:
```
pip3 install -r requirements.txt
pip3 install -e src/
```

## Testing
```
make up
make test
## or, to run individual test types
make unit
make e2e
```
#### or, if you have a local virtualenv
```
make up
pytest tests/unit
pytest tests/integration
pytest tests/e2e
```

#### to see app logs from the container
```
make logs
```