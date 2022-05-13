import uuid
from decimal import Decimal
from typing import List

class Entity:
    def __init__(self, id: str):
        self.id = id

class Account(Entity):
    def __init__(self, initialCredit: Decimal):
        id = uuid.uuid4()
        super().__init__(str(id))        
        self.balance = initialCredit

class Customer(Entity):
    def __init__(self, firstName: str, lastName:str, customerId: str):
        super().__init__(customerId)
        self.firstName = firstName
        self.lastName = lastName
        self.accounts: List[Account] = []
    
    def openAccount(self, initialCredit: Decimal) -> Account:
        acc = Account(initialCredit)
        self.accounts.append(acc)
        return acc
    
    def calculateBalance(self) -> Decimal:
        balance = 0
        for acc in self.accounts:
            balance += acc.balance
        return balance

class Transaction(Entity):
    def __init__(self, accountId: str, customerId: str, amount: Decimal):
        id = uuid.uuid4()
        super().__init__(str(id))
        self.amount = amount
        self.accountId = accountId
        self.customerId = customerId
