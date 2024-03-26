import socket

def read_ascii() -> str:
    data = ''
    while True:
        line = input()
        if not line: break
        else: data += line + '\n'
    return data


PORT = 9000
HOST = "127.0.0.1"
print("You are connecting to 127.0.0.1:9000")

nickname = input("Please tell us your nickname : ")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # send nickname
    s.send(nickname.encode('utf-8'))
    
    while True:
        # send the actual message
        msg = input(">>>")
        if msg == "U":
            msg = read_ascii()
            
        else:
            s.send(msg.encode('utf-8'))
            print(f"message sent: {msg}")
