import select
import socket
import threading as t
import sys

from typing import Dict, Tuple
from utils import Address, Message, MessageType, Disconnected


def read_ascii() -> str:
    data = ''
    while True:
        line = input()
        if not line: break
        else: data += line + '\n'
    return data

class Client:
    def __init__(self):
        self._tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.nickname = None
        self.inputs = [ sys.stdin, self._tcp_socket, self._udp_socket]

    def initialize_connection(self, addr: Address):
        self._connect(addr)
        self._addr = addr
        msg = Message.decode(client._receive_message_tcp())
        print(msg.get_msg())
        # get nickname
        nickname = input("")
        self.nickname = nickname
        nickname_msg = Message(self.nickname, nickname, MessageType.NICKNAME.value)
        self._send_message_tcp(nickname_msg.encode())
        msg = Message.decode(client._receive_message_tcp())
        print(msg.get_msg())
        print("Commands:\n 'U' - send ascii art,\n 'D' - disconnect ")

    def _connect(self, addres: Address):
        self._tcp_socket.connect(addres)

    def _send_message_tcp(self, msg: bytes):
        self._tcp_socket.send(msg)

    def _send_message_udp(self, msg: bytes):
        self._udp_socket.sendto(msg, self._addr)

    def _receive_message_tcp(self) -> bytes:
        return self._tcp_socket.recv(1024)
    
    def _receive_message_udp(self) -> bytes:
        return self._udp_socket.recv(1024)
    
    def handle_connections(self):
        while True:
            inputs, _, _ = select.select(self.inputs, [], [])
            for ready_input in inputs:
                if ready_input == sys.stdin:
                    input = sys.stdin.readline()
                    if input.strip('\n') == "U":
                        print("---enter the ascii chcaracter and press enter two times---")
                        data = read_ascii()
                        msg = Message(self.nickname, data, MessageType.CLIENT_TO_SERVER.value)
                        self._send_message_udp(msg.encode())
                        print("---message ent---")
                    elif input.strip('\n') == "D":
                        msg = Message(self.nickname, input.strip('\n'), MessageType.DISCONNECT.value)
                        self._send_message_tcp(msg.encode())
                        raise Disconnected
                    elif len(input) > 1:
                        msg = Message(self.nickname, input.strip('\n'), MessageType.CLIENT_TO_SERVER.value)
                        self._send_message_tcp(msg.encode())
                elif ready_input == self._tcp_socket:
                    # print("got a message!")
                    data = self._receive_message_tcp()
                    if len(data) > 0:
                        msg = Message.decode(data)
                        print(msg.chat_entry())
                    else:
                        raise Disconnected
                elif ready_input == self._udp_socket:
                    print("udp")
                    msg = Message.decode(self._receive_message_udp())
                    print(msg)


if __name__ == "__main__":
    client = Client()
    try:
        client.initialize_connection(("localhost", 9001))
        client.handle_connections()
    except KeyboardInterrupt:
        client._tcp_socket.close()
    except Disconnected:
        client._tcp_socket.close()
        print("disconnected from server")
    # finally:
    #     client._tcp_socket.close()