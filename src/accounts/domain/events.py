from dataclasses import dataclass
from typing import NewType, Callable, List

class Event:
    pass

@dataclass
class AccountOpened(Event):
    customerId: str
    accountId: str

Handler = NewType("Handler", Callable[[Event], List[Event]])