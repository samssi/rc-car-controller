import json
import pygame
from config import Settings

settings = Settings('settings.ini')


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class KeyboardControlState(metaclass=Singleton):
    def __init__(self):
        self.keyboard_event_emit_timer = settings.getParser().getint('default', 'udp_event_emit_timer_interval')
        self.keyboard_control_timer = settings.getParser().getint('default', 'keyboard_reset_timer_interval')
        self.new_direction_event = False
        self.new_steering_event = False
        self.direction = 0
        self.steering = 0
        self.keyboard_control_event = pygame.USEREVENT + 1
        self.keyboard_reset_event = pygame.USEREVENT + 2

    def update_direction(self, direction):
        self.direction += self._check_range(direction, self.direction)
        self.new_direction_event = True

    def update_steering(self, steering):
        self.steering += self._check_range(steering, self.steering)
        self.new_steering_event = True

    @staticmethod
    def _check_range(new, current):
        return new if 100 >= current + new >= -100 else 0

    def to_event_queue(self):
        pygame.time.set_timer(self.keyboard_reset_event, self.keyboard_control_timer)
        pygame.time.set_timer(self.keyboard_control_event, self.keyboard_event_emit_timer)
        keyboard_control_event = pygame.event.Event(self.keyboard_control_event)
        keyboard_reset_event = pygame.event.Event(self.keyboard_reset_event)
        pygame.event.post(keyboard_control_event)
        pygame.event.post(keyboard_reset_event)

    def to_control_command(self):
        state = {
            "control":
                {
                    "direction": self.direction,
                    "steering": self.steering
                }
        }

        json_message = json.dumps(state)
        return json_message
