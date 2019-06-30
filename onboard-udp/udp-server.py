import socket
import json
import RPi.GPIO as GPIO

host_and_port = ("0.0.0.0", 6789)

# See: http://www.ti.com/lit/ds/symlink/l293.pdf
enable_channel_1_and_2 = 3
driver_input_1A = 13
driver_input_2A = 15

enable_channel_3_and_4 = 5
driver_input_3A = 11
driver_input_4A = 7


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    GPIO.setup(enable_channel_1_and_2, GPIO.OUT)
    GPIO.setup(driver_input_1A, GPIO.OUT)
    GPIO.setup(driver_input_2A, GPIO.OUT)

    GPIO.setup(enable_channel_3_and_4, GPIO.OUT)
    GPIO.setup(driver_input_3A, GPIO.OUT)
    GPIO.setup(driver_input_4A, GPIO.OUT)

    GPIO.output(enable_channel_1_and_2, GPIO.HIGH)
    GPIO.output(enable_channel_3_and_4, GPIO.HIGH)


def steer(command):
    if command['steering']['direction'] == 'left':
        GPIO.output(driver_input_1A, GPIO.HIGH)
        GPIO.output(driver_input_2A, GPIO.LOW)
    elif command['steering']['direction'] == 'right':
        GPIO.output(driver_input_1A, GPIO.LOW)
        GPIO.output(driver_input_2A, GPIO.LOW)
    elif command['steering']['direction'] == 'accelerate':
        GPIO.output(driver_input_3A, GPIO.HIGH)
        GPIO.output(driver_input_4A, GPIO.LOW)
    elif command['steering']['direction'] == 'decelerate':
        GPIO.output(driver_input_3A, GPIO.LOW)
        GPIO.output(driver_input_4A, GPIO.LOW)


def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(host_and_port)
    return server


def run(server):
    print("Starting onboard UDP server")
    try:
        while True:
            data, _ = server.recvfrom(1024)
            print(f"UDP message received: {data}")
            json_dict = json.loads(data)
            steer(json_dict)

    except KeyboardInterrupt:
        server.close()
        print('\nUDP server shutdown')

setup()
run(server())