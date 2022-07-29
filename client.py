import socket

HOST = "127.0.0.1"
PORT = 54321

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((HOST, PORT))
server_socket.sendall(b"Test")
data = server_socket.recv(1024)

print(f"Response: {data}")
