import pygame
import pygame.locals
import sys
import cv2
from config import Settings
from controller import keyboard

settings = Settings('settings.ini')

udp_client_enabled = settings.getParser().getboolean('default', 'udp_client_enabled')
video_enabled = settings.getParser().getboolean('default', 'video_streaming_enabled')
width_height = (settings.getParser().getint('default', 'window_width'), settings.getParser().getint('default', 'window_height'))
video_stream_url = (settings.getParser().get('default', 'video_stream_url'))

if video_enabled:
    stream = cv2.VideoCapture(video_stream_url)


def init():
    pygame.init()
    keyboard.init_keyboard()
    return create_window()


def create_window():
    black_color = (0, 0, 0)
    window = pygame.display.set_mode(width_height, 0, 32)
    window.fill(black_color)
    keyboard.init_keyboard()
    return window


def shutdown():
    print("Exiting")
    pygame.quit()
    cv2.destroyAllWindows()
    sys.exit()


def listen_keyboard():
    for event in pygame.event.get():
        if event.type == pygame.locals.KEYDOWN:
            keyboard.determine_key()
        elif event.type == pygame.QUIT:
            shutdown()


def read_camera_stream():
    grabbed, frame = stream.read()
    return frame


def start():
    print('Use WASD to send control commands. Other keys will terminate the client')
    window = init()
    while True:
        if video_enabled:
            frame = pygame.surfarray.make_surface(read_camera_stream())
            window.blit(frame, (0, 0))

        listen_keyboard()
        pygame.display.update()


if __name__ == "__main__":
    start()

