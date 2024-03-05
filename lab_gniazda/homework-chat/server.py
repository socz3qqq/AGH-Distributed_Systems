import socket
import threading as t

def client_thread(socket: socket.socket, name: str) -> t.Thread:
    return t.Thread(target=client_thread_routine, name=name, args=socket)

def client_thread_routine(socket: socket.socket) -> None:
    buff = []
    adress = ""
    print("Hello from client thread")
    buff, address = socket.recvfrom()
    print(buff, address)


if __name__ == '__main__':
    print("Python TCP Server...")

    MAX_CONNECTIONS = 10
    HOST = '127.0.0.1'
    PORT = 9000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(MAX_CONNECTIONS)
        print(f"Listening on : {HOST}:{PORT}")
        # main loop of the server
        while True:
            with server_socket.accept() as ( client_socket, address):
                print("client connected")
                ct = client_thread(client_socket, address)
                ct.run()