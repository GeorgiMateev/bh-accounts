from typing import List, Optional

from accounts.repositories import repository
from accounts.domain import model

class CustomersInMemoryRepository(repository.AbstractRepository):
    def __init__(self, initialCustomers: List[model.Customer]):
        super().__init__()
        self.customers = initialCustomers

    def get(self, id: str) -> Optional[model.Customer]:
        result = next(filter(lambda c: c.id == id, self.customers), None)
        return result
        

    def add(self, customer: model.Customer):
        self.customers.append(customer)

    def list(self) -> List[model.Customer]:
        return self.customers


