import uuid

from accounts.repositories import customers, transactions
from accounts.services import customers as service
from accounts.domain import commands, model, queries, events


def get_new_repos():
    transactionsRepo = transactions.TransactionsInMemoryRepository()

    customer = model.Customer("Georgi", "Mateev", str(uuid.uuid4()))
    customersRepo = customers.CustomersInMemoryRepository([customer])

    return (customersRepo, transactionsRepo)

def test_open_account():
    repos = get_new_repos()
    customersRepo = repos[0]
    transactionsRepo = repos[1]
    customerService = service.Customers(customersRepo, transactionsRepo)

    customers = customersRepo.list()
    targetCustomer = customers[0]

    command1 = commands.OpenAccount(customerId = targetCustomer.id, initialCredit=10)
    acc1 = customerService.openAccount(command1)[0]
    assert type(acc1) == events.AccountOpened
    assert acc1.accountId != ""

    command2 = commands.OpenAccount(customerId = targetCustomer.id, initialCredit=10.54)
    acc2 = customerService.openAccount(command2)[0]
    assert type(acc2) == events.AccountOpened
    assert acc2.accountId != ""

    query = queries.CustomerHistory(customerId=targetCustomer.id)
    customerView = customerService.queryCustomerHistory(query)

    assert type(customerView) == queries.CustomerView

    assert customerView.balance == 20.54
    assert customerView.customerId == targetCustomer.id
    assert sum([t.amount for t in customerView.transactions]) == 20.54

def test_open_account_without_transaction():
    repos = get_new_repos()
    customersRepo = repos[0]
    transactionsRepo = repos[1]
    customerService = service.Customers(customersRepo, transactionsRepo)

    customers = customersRepo.list()
    targetCustomer = customers[0]

    command1 = commands.OpenAccount(customerId = targetCustomer.id, initialCredit=0)
    customerService.openAccount(command1)[0]

    query = queries.CustomerHistory(customerId=targetCustomer.id)
    customerView = customerService.queryCustomerHistory(query)
    assert len(customerView.transactions) == 0
    assert len(transactionsRepo.list()) == 0

def test_open_account_with_negative_credit():
    repos = get_new_repos()
    customersRepo = repos[0]
    transactionsRepo = repos[1]
    customerService = service.Customers(customersRepo, transactionsRepo)

    customers = customersRepo.list()
    targetCustomer = customers[0]

    command1 = commands.OpenAccount(customerId = targetCustomer.id, initialCredit=-1)
    try:
        customerService.openAccount(command1)
    except:
        assert True
        return

    assert False
