import socket
from config import Settings

host_and_port = ("192.168.1.127", 6789)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

settings = Settings('settings.ini')
udp_client_enabled = settings.getParser().getboolean('default', 'udp_client_enabled')


def send(command):
    if udp_client_enabled:
        client.sendto(bytes(command, 'utf8'), host_and_port)
    print(command)
