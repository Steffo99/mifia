from typing import Type, List
from .events import Event


class EventList:
    def __init__(self, li=None):
        if li is None:
            self.list: List[Event] = []
        else:
            self.list = li

    def __len__(self):
        return len(self.list)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.list)})"

    def add(self, event: Event):
        self.list.append(event)

    def remove(self, event: Event):
        self.list.remove(event)

    def get_first_event_of_type(self, event_type: Type[Event]) -> Event:
        for event in self.list:
            if isinstance(event, event_type):
                return event
        return None
