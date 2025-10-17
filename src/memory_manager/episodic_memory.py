class EpisodicMemory:
    def __init__(self):
        self.events = []

    def store_event(self, event):
        self.events.append(event)

    def get_events(self):
        return self.events
