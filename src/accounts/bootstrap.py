import logging

from accounts import config
from accounts.repositories import transactions, customers
from accounts.services import messagebus, customers as service
from accounts.domain import events, commands, queries, model

logger = logging.getLogger(__name__)

def bootstrap() -> messagebus.MessageBus:
    transactionsRepo = transactions.TransactionsInMemoryRepository()

    customer = model.Customer("Georgi", "Mateev", config.initialCustomerId())
    customersRepo = customers.CustomersInMemoryRepository([customer])

    customersService = service.Customers(customersRepo, transactionsRepo)

    eventHandles = {
        events.AccountOpened: [lambda e: logger.debug("handled event %s", e)]
    }

    commandHandlers = {
        commands.OpenAccount: lambda e: customersService.openAccount(e)
    }

    queryHandlers = {
        queries.CustomerHistory: lambda e: customersService.queryCustomerHistory(e)
    }

    bus = messagebus.MessageBus(eventHandles, commandHandlers, queryHandlers)

    return bus