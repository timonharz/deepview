class EventBus:
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_type, listener):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def notify(self, event_type, data):
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                listener(data)
                

bus = EventBus()

def listener1(data):
    print(f"Listener 1 received data: {data}")

def listener2(data):
    print(f"Listener 2 received data: {data}")

bus.subscribe("test", listener1)