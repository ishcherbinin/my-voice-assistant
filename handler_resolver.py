from typing import Callable


class HandlerResolver:

    """Iterates through handler lists and call each. Guard condition should be inside handler."""

    def __init__(self, handlers: list[Callable]):
        self._handlers = handlers


    def resolve(self, command: str):
        for handler in self._handlers:
            handler(command)