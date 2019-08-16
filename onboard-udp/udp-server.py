import socket
import json
import time
import threading
import RPi.GPIO as GPIO
from config import Settings
from state import CarState

carState = CarState()

settings = Settings('settings.ini')
host = settings.getParser().get('default', 'udp_server_accept_host')
port = settings.getParser().getint('default', 'udp_server_port')

cutoff_polling_frequency_in_secs = settings.getParser().getint('default', 'cutoff_polling_frequency_in_secs')

host_and_port = (host, port)

# See: http://www.ti.com/lit/ds/symlink/l293.pdf
enable_channel_1_and_2 = 3
driver_input_1A = 13
driver_input_2A = 15

enable_channel_3_and_4 = 5
driver_input_3A = 11
driver_input_4A = 7

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

# DC electric motors: 5-10 kHz or higher
driver_input_1A_pwm = GPIO.PWM(driver_input_1A, 7500)


def cut_engine():
    print("No UDP control messages received! Cutting engine!")
    GPIO.output(driver_input_1A, GPIO.LOW)
    GPIO.output(driver_input_2A, GPIO.LOW)
    GPIO.output(driver_input_3A, GPIO.LOW)
    GPIO.output(driver_input_4A, GPIO.LOW)
    driver_input_1A_pwm.stop()


def steer(command):
    if int(command['control']['steering']) > 0: #left
        print('go left')
        GPIO.output(driver_input_3A, GPIO.HIGH)
        GPIO.output(driver_input_4A, GPIO.LOW)
    elif int(command['control']['steering']) < 0: #right
        print('go right')
        GPIO.output(driver_input_3A, GPIO.LOW)
        GPIO.output(driver_input_4A, GPIO.HIGH)
    elif int(command['control']['direction']) > 0: #accelerate'
        print('accelerate')
        GPIO.output(driver_input_2A, GPIO.LOW)
        driver_input_1A_pwm.start(float(command['control']['direction']))
    elif command['control']['direction'] < 0: #decelerate
        print('decelerate')
        driver_input_1A_pwm.stop()
        GPIO.output(driver_input_2A, GPIO.LOW)



def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(host_and_port)
    return server


def cutoff():
    thread = threading.currentThread()

    while getattr(thread, "do_run", True):
        if carState.cutoff_threshold_passed():
            cut_engine()

        time.sleep(cutoff_polling_frequency_in_secs)

    print('Cutoff thread finished')


def run(server):
    print("Starting onboard UDP server")
    cutoff_thread = threading.Thread(target=cutoff)
    cutoff_thread.start()

    try:
        while True:
            data, _ = server.recvfrom(1024)
            carState.update_time()
            print(f"UDP message received: {data}")
            json_dict = json.loads(data)
            steer(json_dict)

    except KeyboardInterrupt:
        server.close()
        cutoff_thread.do_run = False
        cutoff_thread.join()
        print('\nUDP server shutdown')


if __name__ == "__main__":
    run(server())
