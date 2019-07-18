import pygame
import json
from udp import udp
from event import KeyboardControlState
from config import Settings

settings = Settings('settings.ini')

left_key = settings.getParser().getint('default', 'keyboard_left')
right_key = settings.getParser().getint('default', 'keyboard_right')
up_key = settings.getParser().getint('default', 'keyboard_up')
down_key = settings.getParser().getint('default', 'keyboard_down')

keyboardControlState = KeyboardControlState()


def init_keyboard():
    pygame.key.set_repeat(1, 1)


def determine_key():
    keys = pygame.key.get_pressed()

    if keys[left_key]:
        keyboardControlState.update_steering(-10)
        keyboardControlState.new_steering_event = True
    if keys[right_key]:
        keyboardControlState.update_steering(10)
        keyboardControlState.new_steering_event = True

    if keys[down_key]:
        keyboardControlState.update_direction(-10)
        keyboardControlState.new_direction_event = True
        #udp.send(json_control_command("accelerate"))
    if keys[up_key]:
        keyboardControlState.update_direction(10)
        keyboardControlState.new_direction_event = True

    keyboardControlState.to_event_queue()
