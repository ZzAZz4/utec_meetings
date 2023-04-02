
from collections import defaultdict


class StaticEventHandler:
    def __init__(self, *event_types):
        self._handlers = {event_type: [] for event_type in event_types}

    def link(self, event, handler):
        if event not in self._handlers:
            raise ValueError(f"Event type {event} not supported")

        self._handlers[event].append(handler)

    def unlink(self, event, handler):
        if event not in self._handlers:
            raise ValueError(f"Event type {event} not supported")
        self._handlers[event].remove(handler)

    def fire(self, event, *args, **kwargs):
        for handler in self._handlers[event]:
            handler(event, *args, **kwargs)


class DynamicEventHandler:
    def __init__(self):
        self._handlers = defaultdict(list)

    def link(self, event, handler):
        self._handlers[event].append(handler)

    def unlink(self, event, key):
        self._handlers[event].remove(key)

    def fire(self, event, *args, **kwargs):
        if event not in self._handlers:
            return

        for handler in self._handlers[event]:
            handler(event, *args, **kwargs)
