import time


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CarState(metaclass=Singleton):
    def __init__(self):
        self.last_message_received = self.current_time_in_millis()

    @staticmethod
    def current_time_in_millis():
        return int(round(time.time() * 1000))

    def cutoff_threshold(self):
        return self.last_message_received + 1200

    def cutoff_threshold_passed(self):
        return self.cutoff_threshold() < self.current_time_in_millis()

    def update_time(self):
        self.last_message_received = self.current_time_in_millis()
