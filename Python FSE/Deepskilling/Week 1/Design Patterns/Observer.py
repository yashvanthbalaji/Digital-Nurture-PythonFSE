class Observer:
    def update(self, message):
        print("Received:", message)


class Subject:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify(self, message):
        for observer in self.observers:
            observer.update(message)


obj1 = Observer()
obj2 = Observer()

subject = Subject()

subject.add_observer(obj1)
subject.add_observer(obj2)

subject.notify("New Message")