import pygame
import pygame.locals
import sys
import cv2
from udp import udp
from config import Settings
from controller import keyboard
from event import KeyboardControlState

settings = Settings('settings.ini')
keyboardControlState = KeyboardControlState()

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
    window = pygame.display.set_mode(width_height)
    window.fill(black_color)
    keyboard.init_keyboard()
    return window


def shutdown():
    print("Exiting")
    pygame.quit()
    cv2.destroyAllWindows()
    sys.exit()


def listen_events():
    for event in pygame.event.get():
        if event.type == pygame.locals.KEYDOWN:
            keyboard.determine_key()
        elif event.type == pygame.QUIT:
            shutdown()
        elif event.type == keyboardControlState.keyboard_control_event:
            udp.send(keyboardControlState.to_control_command())
        elif event.type == keyboardControlState.keyboard_reset_event:
            _handle_keyboard_reset_event()
            keyboardControlState.new_direction_event = False
            keyboardControlState.new_steering_event = False


def _handle_keyboard_reset_event():
    print(f'new direction event: {keyboardControlState.new_direction_event}')
    print(f'new steering event: {keyboardControlState.new_steering_event}')
    if not keyboardControlState.new_direction_event:
        if keyboardControlState.direction > 0:
            keyboardControlState.update_direction(-10)
        elif keyboardControlState.direction < 0:
            keyboardControlState.update_direction(10)

    if not keyboardControlState.new_steering_event:
        if keyboardControlState.steering > 0:
            keyboardControlState.update_steering(-10)
        elif keyboardControlState.steering < 0:
            keyboardControlState.update_steering(10)


def read_camera_stream():
    grabbed, frame = stream.read()
    return frame


def start():
    print('Use WASD to send control commands. Other keys will terminate the client')
    window = init()
    while True:
        if video_enabled:
            frame = read_camera_stream()

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, width_height)
            frame = frame.swapaxes(0, 1)
            frame = pygame.surfarray.make_surface(frame)

            window.blit(frame, (0, 0))

        listen_events()
        pygame.display.update()


if __name__ == "__main__":
    start()

