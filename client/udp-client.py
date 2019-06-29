import socket
import json
import pygame
import pygame.locals
import sys

#host_and_port = ("127.0.0.1", 6789)
host_and_port = ("192.168.1.127", 6789)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

left_key = pygame.K_a
right_key = pygame.K_d
up_key = pygame.K_w
down_key = pygame.K_s


def init():
    pygame.init()
    create_window()
    init_keyboard()


def init_keyboard():
    pygame.key.set_repeat(1, 10)


def create_window():
    black_color = (0, 0, 0)
    width_and_height = (800, 600)
    window = pygame.display.set_mode(width_and_height, 0, 32)
    window.fill(black_color)
    init_keyboard()


def json_control_command(direction):
    state = {
        "steering":
            {direction: 10, "percentage": 100}}

    return json.dumps(state)


def send(command):
    client.sendto(bytes(command, 'utf8'), host_and_port)


def quit():
    print("Exiting")
    pygame.quit()
    sys.exit()


def determine_key(event):
    if event.key == left_key:
        send(json_control_command("left"))
    elif event.key == right_key:
        send(json_control_command("right"))
    elif event.key == down_key:
        send(json_control_command("decelerate"))
    elif event.key == up_key:
        send(json_control_command("accelerate"))


def start():
    print('Use WASD to send control commands. Other keys will terminate the client')
    init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.locals.KEYDOWN:
                determine_key(event)
            elif event.type == pygame.QUIT:
                quit()


if __name__ == "__main__":
    start()
