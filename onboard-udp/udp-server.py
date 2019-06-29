import socket
import json
import RPi.GPIO as GPIO

relayIn1Left = 29
relayIn2Right = 33
relayIn3Accelerate = 31
relayIn4Decelerate = 35
relayIn5 = 37
relayIn6 = 36
relayIn7 = 38
relayIn8 = 40

host_and_port = ("0.0.0.0", 6789)


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(relayIn1Left, GPIO.OUT)
    GPIO.setup(relayIn2Right, GPIO.OUT)
    GPIO.setup(relayIn3Accelerate, GPIO.OUT)
    GPIO.setup(relayIn4Decelerate, GPIO.OUT)
    GPIO.setup(relayIn5, GPIO.OUT)
    GPIO.setup(relayIn6, GPIO.OUT)
    GPIO.setup(relayIn7, GPIO.OUT)
    GPIO.setup(relayIn8, GPIO.OUT)


def relay(status, relay):
    if status == "off":
        GPIO.output(relay, GPIO.LOW)
    elif status == "on":
        GPIO.output(relay, GPIO.HIGH)


def steer(command):
    if command['steering']['direction'] == 'left':
        relay('on', relayIn1Left)
    elif command['steering']['direction'] == 'right':
        relay('off', relayIn1Left)
    elif command['steering']['direction'] == 'accelerate':
        relay('on', relayIn3Accelerate)
    elif command['steering']['direction'] == 'decelerate':
        relay('off', relayIn3Accelerate)


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