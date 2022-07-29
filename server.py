import socket

#Kind of a hacky way to get local IP using only socket, but works.
def get_local_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	return s.getsockname()[0]

HOST = get_local_ip()
PORT = 54321

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

if s:
	print(f"Server started at {HOST}:{PORT}")

conn, addr = s.accept()
with conn:
	print(f"{addr} connected")
	while True:
		data = conn.recv(1024)
		if not data:
			break
		conn.sendall(data)
