from typing import Callable, Dict, List, Union, Type, TYPE_CHECKING
import logging
from accounts.domain import events, commands, queries

Message = Union[commands.Command, events.Event]

logger = logging.getLogger(__name__)

class MessageBus:
    def __init__(
        self,
        eventHandlers: Dict[Type[events.Event], List[events.Handler]],
        commandHandlers: Dict[Type[commands.Command], commands.Handler],
        queryHandlers: Dict[Type[queries.Query], Callable]
    ):
        self.eventHandlers = eventHandlers
        self.commandHandlers = commandHandlers
        self.queryHandlers = queryHandlers

    def handle(self, message: Message):
        # Initialize a queue of events.
        # Each handler could trigger more events while executing.
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, events.Event):
                effects = self.handleEvent(message)
                self.queue.extend(effects)
            elif isinstance(message, commands.Command):
                effects = self.handleCommand(message)
                self.queue.extend(effects)
            elif isinstance(message, queries.Query):
                return self.handleQuery(message)
            else:
                raise Exception(f"{message} was not an Event or Command")

    def handleEvent(self, event: events.Event):
        side_effects = []
        for handler in self.eventHandlers[type(event)]:
            try:
                logger.debug("handling event %s with handler %s", event, handler)
                effects = handler(event)
                if effects:
                    side_effects.extend(effects)
            except Exception:
                logger.exception("Exception handling event %s", event)
                continue
        return side_effects

    def handleCommand(self, command: commands.Command):
        logger.debug("handling command %s", command)
        try:
            handler = self.commandHandlers[type(command)]
            side_effects = handler(command)
            return side_effects
        except Exception:
            logger.exception("Exception handling command %s", command)
            raise

    def handleQuery(self, query: queries.Query):
        logger.debug("handling query %s", query)
        try:
            handler = self.queryHandlers[type(query)]
            return handler(query)
        except Exception:
            logger.exception("Exception handling query %s", query)
            raise
