from typing import Iterable
from collections import namedtuple
from enum import Enum

Address = namedtuple('Address', ['ip', 'port'])

class Disconnected(BaseException):
    pass

class MessageType(Enum):
    INIT = 1
    NICKNAME = 2
    CLIENT_TO_SERVER = 3
    SERVER_TO_CLIENT = 4
    DISCONNECT = 5

class client():
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address

    def set_credentials(self, id: int, nick: str):
        self.id = id
        self.nick = nick


class IdGenerator():
    def __init__(self, ids: Iterable):
        self.ids = set(ids)

    def next_id(self) -> int:
        return self.ids.pop()
    
    def release(self, id) -> None:
        self.ids.add(id)


class Message:
    """
        | type | author | length | msg |
        type - 1 byte
        author - 10 bytes
        length - 1 byte
        msg - 0 - 256 bytes
    """
    def __init__(self, author: str, msg: str, type: int):
        self._author: str = author
        self._msg: str = msg
        self._type: int = type

    def encode(self) -> bytes:
        type_b = self._type.to_bytes(1, byteorder='big')
        author_b = self._author.encode('utf-8')[:10].ljust(10)
        msg_b = self._msg.encode('utf-8')[:256]
        len_b = len(msg_b).to_bytes(1, byteorder='big')

        return type_b + author_b + len_b + msg_b
    
    def set_type(self, type: MessageType):
        self._type = type
    
    @staticmethod
    def decode(msg_b: bytes) -> "Message":
        n = msg_b[11]
        return Message(msg_b[1:11].decode('utf-8'), msg_b[12:(12+n)].decode('utf-8'), msg_b[0])
    
    def __str__(self):
        return f"author: {self._author.rstrip()}, msg: {self._msg}, type: {self._type}"
    
    def chat_entry(self):
        return f"{self._author.rstrip()} >>> {self._msg}"

    def get_msg(self)->str:
        return self._msg

if __name__ == "__main__":
    message = Message("adam", "hello its me who you're looking for", MessageType.INIT.value)
    encoded = message.encode()
    print(encoded)
    decoded = Message.decode(encoded)
    print(str(decoded))
    print(decoded.chat_entry())