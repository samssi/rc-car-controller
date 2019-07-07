import socket
import json
import pygame
import pygame.locals
import sys
import cv2

stream = cv2.VideoCapture('http://192.168.1.127:8000/stream.mjpg')
width_height = (960, 540)

#host_and_port = ("127.0.0.1", 6789)
host_and_port = ("192.168.1.127", 6789)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

left_key = pygame.K_a
right_key = pygame.K_d
up_key = pygame.K_w
down_key = pygame.K_s
duty_cycle_up = pygame.K_r
duty_cycle_down = pygame.K_e
percentage = 100


def init():
    pygame.init()
    init_keyboard()
    return create_window()


def init_keyboard():
    pygame.key.set_repeat(1, 10)


def create_window():
    black_color = (0, 0, 0)
    window = pygame.display.set_mode(width_height, 0, 32)
    window.fill(black_color)
    init_keyboard()
    return window


def json_control_command(direction):
    state = {
        "steering":
            {"direction": direction, "percentage": percentage}}

    return json.dumps(state)


def send(command):
    client.sendto(bytes(command, 'utf8'), host_and_port)


def quit():
    print("Exiting")
    pygame.quit()
    cv2.destroyAllWindows()
    sys.exit()


def determine_key():
    global percentage
    keys = pygame.key.get_pressed()
    if keys[left_key]:
        send(json_control_command("left"))
    if keys[right_key]:
        send(json_control_command("right"))
    if keys[down_key]:
        if percentage < 100:
            percentage = percentage + 10
            print(percentage)
        send(json_control_command("accelerate"))
    if keys[up_key]:
        if percentage > -100:
            percentage = percentage - 10
            print(percentage)
        send(json_control_command("accelerate"))


def listen_keyboard():
    for event in pygame.event.get():
        if event.type == pygame.locals.KEYDOWN:
            determine_key()
        elif event.type == pygame.QUIT:
            quit()


def read_camera_stream():
    grabbed, frame = stream.read()
    return frame


def start():
    print('Use WASD to send control commands. Other keys will terminate the client')
    window = init()
    while True:
        frame = pygame.surfarray.make_surface(read_camera_stream())
        listen_keyboard()
        window.blit(frame, (0,0))
        pygame.display.update()


if __name__ == "__main__":
    start()
