import json


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class KeyboardControlState(metaclass=Singleton):
    def __init__(self):
        self.direction = 0
        self.steering = 0

    def update_direction(self, direction):
        self.direction += self._check_range(direction, self.direction)

    def update_steering(self, steering):
        self.steering += self._check_range(steering, self.steering)

    @staticmethod
    def _check_range(new, current):
        return new if 100 >= current + new >= -100 else 0

    def to_control_command(self):
        state = {
            "control":
                {
                    "direction": self.direction,
                    "steering": self.steering
                }
        }

        json_message = json.dumps(state)
        print(json_message)
        return json_message
