import socket, sys, selectors, types

#Kind of a hacky way to get local IP using only socket, but works.
def get_local_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	return s.getsockname()[0]

def accept_conn(s):
	conn, addr = s.accept()
	print(f"{addr} connected")
	conn.setblocking(False)
	data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
	events = selectors.EVENT_READ | selectors.EVENT_WRITE
	sel.register(conn, events, data=data)

def service_conn(key, mask):
	s = key.fileobj
	data = key.data
	if mask & selectors.EVENT_READ:
		recv_data = s.recv(1024)
		if recv_data:
			data.outb += recv_data
		else:
			print(f"Connection to {data.addr} closed.")
			sel.unregister(s)
			s.close()
	if mask & selectors.EVENT_WRITE:
		if data.outb:
			print(f"Sending {data.outb.decode()} to {data.addr}")
			datasent = s.send(data.outb)
			data.outb = data.outb[datasent:]
	
	
sel = selectors.DefaultSelector()

#temporarily hardcoded to localhost for sake of testing convenience
#HOST = get_local_ip()
#HOST = "127.0.0.1"
#PORT = 54321

HOST, PORT = sys.argv[1], int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

if s:
	print(f"Server started at {HOST}:{PORT}")

s.setblocking(False)
sel.register(s, selectors.EVENT_READ, data=None)

try:
	while True:
		events = sel.select(timeout=None)
		for key, mask in events:
			if key.data is None:
				accept_conn(key.fileobj)
			else:
				service_conn(key, mask)
except KeyboardInterrupt:
	print("SIGINT caught, exiting")
finally:
	sel.close()
