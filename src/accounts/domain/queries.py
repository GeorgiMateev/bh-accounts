from dataclasses import dataclass
from typing import List
from decimal import Decimal

class Query:
    pass

class View:
    pass

@dataclass
class CustomerHistory(Query):
    customerId: str

@dataclass
class TransactionView(View):
    id: str
    accountId: str
    amount: Decimal

@dataclass
class CustomerView(View):
    customerId: str
    firstName: str
    lastName: str
    balance: Decimal
    transactions: List[TransactionView]
