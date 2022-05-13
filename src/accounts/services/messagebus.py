from typing import Callable, Dict, List, Union, Type, TYPE_CHECKING
import logging
from accounts.domain import events, commands

Message = Union[commands.Command, events.Event]

logger = logging.getLogger(__name__)

class MessageBus:
    def __init__(
        self,
        event_handlers: Dict[Type[events.Event], List[events.Handler]],
        command_handlers: Dict[Type[commands.Command], commands.Handler],
    ):
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers

    def handle(self, message: Message):
        # Initialize a queue of events.
        # Each handler could trigger more events while executing.
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, events.Event):
                effects = self.handle_event(message)
                self.queue.extend(effects)
            elif isinstance(message, commands.Command):
                effects = self.handle_command(message)
                self.queue.extend(effects)
            else:
                raise Exception(f"{message} was not an Event or Command")

    def handle_event(self, event: events.Event):
        side_effects = []
        for handler in self.event_handlers[type(event)]:
            try:
                logger.debug("handling event %s with handler %s", event, handler)
                effects = handler(event)
                side_effects.extend(effects)
            except Exception:
                logger.exception("Exception handling event %s", event)
                continue
        return side_effects

    def handle_command(self, command: commands.Command):
        logger.debug("handling command %s", command)
        try:
            handler = self.command_handlers[type(command)]
            side_effects = handler(command)
            return side_effects
        except Exception:
            logger.exception("Exception handling command %s", command)
            raise