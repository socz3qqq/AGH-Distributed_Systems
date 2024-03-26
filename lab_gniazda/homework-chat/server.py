import socket
import threading as t

from collections import namedtuple
from utils import client

Address = namedtuple('Address', ['ip', 'port'])

def server_tcp_thread(address: Address, max_connections: int) -> t.Thread:
    print("Creating tcp thread...")
    return t.Thread(target=server_tcp_routine, name='tcp', args=(address, max_connections))

def server_tcp_routine(address: Address, max_connections: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(address)
        server_socket.listen(max_connections)
        print(f"TCP Server Listening on : {address.ip}:{address.port}")
        # main loop of the server
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"client connected: {client_socket}, {client_address}")
            # with client_lock:
            #     clients[]
            # ct = client_thread(client_socket, client_address)
            # ct.start()

def server_udp_thread(address: Address, max_connections: int) -> t.Thread:
    print("Creating udp thread...")
    return t.Thread(target=server_tcp_routine, name='tcp', args=(address, max_connections))

def server_udp_routine(address: Address, max_connections: int):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        buff = []
        addr = '127.0.0.1'

        server_socket.bind(address)
        server_socket.listen(max_connections)
        print(f"UDP Server Listening on : {address.ip}:{address.port}")
        # main loop of the server
        while True:
            buff, addr = server_socket.recvfrom(1024)
            print(f"udp msg received from {addr} : " + str(buff, 'utf-8'))

def client_thread(socket: socket.socket, name: str) -> t.Thread:
    print("Creating udp thread... ")
    return t.Thread(target=client_thread_routine, name=name, args=(socket,))

def client_thread_routine(client_socket: socket.socket) -> None:
    buff = []
    adress = ""
    print("Hello from client thread")
    try:
        buff, address = client_socket.recvfrom(1024)
        print(buff, address)
    finally:
        print("closing connection")
        client_socket.close()


if __name__ == '__main__':

    MAX_CONNECTIONS = 10
    HOST = '127.0.0.1'
    TCP_PORT = 9000
    UDP_PORT = 9000
    
    TCP_ADDRESS = Address(HOST, TCP_PORT)
    UDP_ADDRESS = Address(HOST, UDP_PORT)

    client_lock = t.Lock()
    clients = dict()

    tcp_thread = server_tcp_thread(TCP_ADDRESS, MAX_CONNECTIONS)
    tcp_thread.start()
    # udp_thread = server_udp_thread(UDP_ADDRESS, MAX_CONNECTIONS)
    # udp_thread.start()
