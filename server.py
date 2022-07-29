import socket

HOST = "127.0.0.1"
PORT = 54321

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

conn, addr = server_socket.accept()
with conn:
	print(f"{addr} connected")
	while True:
		data = conn.recv(1024)
		if not data:
			break
		conn.sendall(data)
