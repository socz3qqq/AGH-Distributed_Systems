import socket
import threading as t
import sys

from select import select
from typing import Dict, Callable
from utils import IdGenerator, Address, MessageType, Message
from concurrent.futures import ThreadPoolExecutor

MAX_CLIENTS = 10
BUFF_SIZE = 1024

class Client():
    def __init__(
            self,
            client_socket: socket.socket,
            client_address: Address,
            nickname: str,
            id: int,
            send_cb: Callable[["Client", bytes], None]
    ):
        self._socket: socket.socket = client_socket
        self._address: str = client_address
        self.nickname: str = nickname
        self._id: int = id
        self._buff: bytes = []
        self._send_to_others: callable = send_cb

    def _init(self):
        # ask for a nickname
        print(f"initializing a client with id: {self._id}")
        msg = Message("server", "Enter your nickname: ", MessageType.INIT.value)
        self._socket.send(msg.encode())
        data = Message.decode(self._socket.recv(BUFF_SIZE))
        self.nickname = data._author
        print(str(data))
        msg = Message(
            "server",
            f"Hello {self.nickname}! Enjoy your time here :)",
            MessageType.NICKNAME.value
            )
        self._socket.send(msg.encode())

    def _handle_messages(self):
        while True:
            data = Message.decode(self._socket.recv(BUFF_SIZE))
            print(str(data))
            self._send_to_others(self, data)
          
    def send(self, msg: Message):
        self._socket.send(msg.encode())

    def run(self):
        self._init()
        self._handle_messages()
    
    def close(self):
        self._socket.close()


class ClientList():
    def __init__(self, client_count: int):
        self._clients: Dict[int, Client] = {}
        self._id_generator = IdGenerator(range(client_count))
        self._clients_list_lock = t.RLock()

    def __iter__(self):
        with self._clients_list_lock:
            for client in self._clients.values():
                yield client

    def add_new_client(self, sock: socket.socket, addr: Address) -> Client:
        new_client_id = self._id_generator.next_id()
        client = Client(sock, addr, "unknown", new_client_id, self.send_message)
        with self._clients_list_lock:
            self._clients[new_client_id] = client
        print("added a new client")
        return client
    
    def remove_client(self, client: Client) -> Client:
        with self._clients_list_lock:
            try:
                c = self._clients.pop(client._id)
            except KeyError:
                print("Client not present in the list! ( returning None )")
                return None
        client.close()
        return c

    def send_message(self, sender: Client, msg: Message):
        if msg._type == MessageType.DISCONNECT.value:
            self.remove_client(sender)
            return
        print("forwarding the message to others...")
        with self._clients_list_lock:
            for client in self._clients.values():
                if client != sender:
                    print("trying to reach out to " + client.nickname)
                    client.send(msg)
        print("--done--")
                    

class Server: 
    def __init__(self, max_clients: int):
        self._tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._clients = ClientList(max_clients)
        self._thread_pool = ThreadPoolExecutor(max_workers=5)

    def accept_connections(self, address: Address):
        self._tcp_socket.bind(address)
        self._tcp_socket.listen()

        self._udp_socket.bind(address)

        while True:
            try:
                sockets, _, _ = select([self._tcp_socket, self._udp_socket], [], [])
            except KeyboardInterrupt:
                self._destroy()
            for ready_socket in sockets:
                if ready_socket == self._tcp_socket:
                    self._handle_tcp_connection()
                elif ready_socket == self._udp_socket:
                    self._handle_udp_messages()
                for client in self._clients:
                    print(f"{client.nickname}")

    def _handle_tcp_connection(self):
        client_socket, client_address = self._tcp_socket.accept()
        client = self._clients.add_new_client(client_socket, client_address)
        self._thread_pool.submit(client.run)
        print(f"client connected: {client_socket}, {client_address}")

    def _handle_udp_messages(self):
        print("received udp")
        data, addr = self._udp_socket.recvfrom(2048)
        print(data)
        for client in self._clients:
            if client._address != addr:
                self._udp_socket.sendto(data, client._address)

    def _destroy(self):
        print("closing server...")
        for client in self._clients:
            print("closing client...")
            client.close()
        self._tcp_socket.close()
        self._udp_socket.close()
        sys.exit(0)


if __name__ == '__main__':
    address = Address('localhost', 9001) 

    server = Server(MAX_CLIENTS)
    print(f"Server started on: {address}")
    server.accept_connections(address)
