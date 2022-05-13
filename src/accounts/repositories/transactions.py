import abc
from typing import List, Optional
from accounts.repositories import repository
from accounts.domain import model

class TransactionsRepository(repository.AbstractRepository):
    @abc.abstractmethod
    def getByCustomer(self, id: str) -> List[model.Transaction]:
        raise NotImplementedError

class TransactionsInMemoryRepository(repository.AbstractRepository):
    def __init__(self):
        super().__init__()
        self.transactions: List[model.Transaction] = []

    def get(self, id: str) -> Optional[model.Transaction]:
        result = next(filter(lambda c: c.id == id, self.transactions), None)
        return result

    def add(self, transaction: model.Transaction):
        self.transactions.append(transaction)

    def getByCustomer(self, id: str) -> List[model.Transaction]:
        result = filter(lambda t: t.customerId == id, self.transactions)
        return result

    def list(self) -> List[model.Transaction]:
        return self.transactions
