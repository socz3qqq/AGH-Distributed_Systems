import socket

PORT = 9000
HOST = "127.0.0.1"
msg = "test message"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.sendto(bytes(msg, 'cp1250'), (HOST, PORT))