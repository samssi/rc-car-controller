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
    pygame.key.set_repeat(1, 10)


def determine_key():
    keys = pygame.key.get_pressed()

    if keys[left_key]:
        keyboardControlState.update_direction(-10)
    if keys[right_key]:
        keyboardControlState.update_direction(10)

    if keys[down_key]:
        keyboardControlState.update_steering(-10)
        #udp.send(json_control_command("accelerate"))
    if keys[up_key]:
        keyboardControlState.update_steering(10)


def json_control_command(direction):
    state = {
        "steering":
            {"direction": direction, "percentage": percentage}}

    return json.dumps(state)
