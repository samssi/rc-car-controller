import socket
from config import Settings

settings = Settings('settings.ini')
udp_client_enabled = settings.getParser().getboolean('default', 'udp_client_enabled')
udp_host = settings.getParser().get('default', 'udp_host')
udp_port = settings.getParser().getint('default', 'udp_port')

host_and_port = (udp_host, udp_port)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send(command):
    if udp_client_enabled:
        client.sendto(bytes(command, 'utf8'), host_and_port)
    print(f'Sending UDP message to {host_and_port}: {command}')
