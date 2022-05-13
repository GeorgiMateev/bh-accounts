# bh-accounts
Managing financial accounts

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
pytest tests/unit
```