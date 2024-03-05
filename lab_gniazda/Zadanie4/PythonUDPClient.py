import socket

serverIP = "127.0.0.1"
serverPort = 9004
msg = "hello there"

print("PYTHON UDP CLIENT | ASSIGNMENT 4")
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

new_msg = b'\01' + bytes(msg, "utf-8")

print(new_msg[0])

client.sendto(b'\xff' + bytes(msg, "utf-8"), (serverIP, serverPort))
