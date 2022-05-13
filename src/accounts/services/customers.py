from decimal import Decimal
from typing import List, Optional
from accounts.domain import model, commands, queries, events, queries
from accounts.repositories import customers, repository, transactions


class InvalidAmount(Exception):
    pass

class Customers:
    def __init__(self,
        customersRepo: repository.AbstractRepository,
        transactionsRepo: transactions.TransactionsRepository):
        self.customersRepo = customersRepo
        self.transactionsRepo = transactionsRepo

    def openAccount(self, command: commands.OpenAccount) -> List[events.Event]:
        if command.initialCredit < 0:
            raise InvalidAmount("Accoount cannot be open with negative credit")

        customer = self.customersRepo.get(command.customerId)
        acc = customer.openAccount(command.initialCredit)

        if command.initialCredit > 0:
            t = model.Transaction(acc.id, customer.id, command.initialCredit)
            self.transactionsRepo.add(t)
        
        return [events.AccountOpened(customer.id, acc.id)]

    def queryCustomerHistory(self, query: queries.CustomerHistory) -> Optional[queries.CustomerView]:
        customer = self.customersRepo.get(query.customerId)
        if not customer:
            return None
        balance = customer.calculateBalance()
        transactions = self.transactionsRepo.getByCustomer(customer.id)

        tView = [queries.TransactionView(t.id, t.accountId, t.amount) for t in transactions]

        view = queries.CustomerView(
            customerId=customer.id,
            firstName=customer.firstName,
            lastName=customer.lastName,
            balance=balance,
            transactions=tView
        )

        return view