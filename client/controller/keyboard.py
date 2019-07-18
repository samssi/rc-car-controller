import pygame
import json
from udp import udp
from event import KeyboardControlState

left_key = pygame.K_a
right_key = pygame.K_d
up_key = pygame.K_w
down_key = pygame.K_s
duty_cycle_up = pygame.K_r
duty_cycle_down = pygame.K_e

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
