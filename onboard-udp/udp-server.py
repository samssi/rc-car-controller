import socket
import json

host_and_port = ("0.0.0.0", 6789)


def steer(command):
    print(command['steering'])


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
            print(json_dict)

    except KeyboardInterrupt:
        server.close()
        print('\nUDP server shutdown')


run(server())