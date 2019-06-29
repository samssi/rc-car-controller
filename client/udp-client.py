import socket
import json

host_and_port = ("192.168.1.127", 6789)
#host_and_port = ("127.0.0.1", 6789)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def json_control_command():
    state = {
        "steering":
            { "left": 10, "percentage": 100 }}

    return json.dumps(state)

def send(command):
    client.sendto(command, host_and_port)

send(json_control_command())