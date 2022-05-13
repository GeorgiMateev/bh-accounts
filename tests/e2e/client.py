from flask import Response
import requests
from decimal import Decimal
from accounts import config

def openAccount(customerId: str, credit: Decimal):
    url = config.getApiUrl()
    r = requests.post(
        f"{url}/{customerId}/open", json={"credit":credit}
    )
    return r

def accountDetails(customerId: str) -> Response:
    url = config.getApiUrl()
    r = requests.get(
        f"{url}/{customerId}"
    )

    return r