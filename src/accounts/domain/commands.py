from dataclasses import dataclass
from decimal import Decimal
from typing import NewType, Callable, List
from accounts.domain import events

class Command:
    pass

@dataclass
class OpenAccount(Command):
    customerId: str
    initialCredit: Decimal

Handler = NewType("Handler", Callable[[Command], List[events.Event]])