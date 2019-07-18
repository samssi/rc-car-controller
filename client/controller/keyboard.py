import pygame
import json
from udp import udp

left_key = pygame.K_a
right_key = pygame.K_d
up_key = pygame.K_w
down_key = pygame.K_s
duty_cycle_up = pygame.K_r
duty_cycle_down = pygame.K_e
percentage = 100


def init_keyboard():
    pygame.key.set_repeat(1, 10)


def determine_key():
    global percentage
    keys = pygame.key.get_pressed()
    if keys[left_key]:
        udp.send(json_control_command("left"))
    if keys[right_key]:
        udp.send(json_control_command("right"))
    if keys[down_key]:
        if percentage < 100:
            percentage = percentage + 10
        udp.send(json_control_command("accelerate"))
    if keys[up_key]:
        if percentage > -100:
            percentage = percentage - 10
            udp.send(json_control_command("accelerate"))


def json_control_command(direction):
    state = {
        "steering":
            {"direction": direction, "percentage": percentage}}

    return json.dumps(state)
