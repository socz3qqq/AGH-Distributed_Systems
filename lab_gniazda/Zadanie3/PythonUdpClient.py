import socket;

serverIP = "127.0.0.1"
serverPort = 9003
msg_bytes = (300).to_bytes(4, byteorder='little')

print('PYTHON UDP CLIENT')
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("sending bytes: ", repr(msg_bytes))
client.sendto(msg_bytes, (serverIP, serverPort))

response = client.recv(4)

print(int.from_bytes(response, byteorder='big'))




