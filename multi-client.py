import socket, sys, selectors, types

sel = selectors.DefaultSelector()

#temporarily hardcoded to localhost for sake of testing convenience
#HOST = input("Enter IP to connect to: ") 
#HOST = "127.0.0.1"
#PORT = 54321

messages = [b"Message 1", b"Message 2"]

def start_conn(host, port, num_conn):
	server_addr = (host, port)
	for i in range (0, num_conn):
		connid = i + 1
		print(f"Connection {connid}: {server_addr}")
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setblocking(False)
		s.connect_ex(server_addr)
		events = selectors.EVENT_READ | selectors.EVENT_WRITE
		data = types.SimpleNamespace(
			connid=connid,
			msg_total=sum(len(m) for m in messages),
			recv_total=0,
			messages=messages.copy(),
			outb=b"",
		)
		sel.register(s, events, data=data)

def service_conn(key, mask):
	s = key.fileobj
	data = key.data
	if mask & selectors.EVENT_READ:
		recv_data = s.recv(1024)
		if recv_data:
			print(f"From connection {data.connid}: {recv_data.decode()}")
			data.recv_total += len(recv_data)
		if not recv_data or data.recv_total == data.msg_total:
			print(f"Connection {data.connid} closed.")
			sel.unregister(s)
			s.close()
	if mask & selectors.EVENT_WRITE:
		if not data.outb and data.messages:
			data.outb = data.messages.pop(0)
		if data.outb:
			print(f"Send: {data.outb.decode()} to connection {data.connid}")
			datasent = s.send(data.outb)
			data.outb = data.outb[datasent:]

HOST, PORT, NUM_CONN = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

start_conn(HOST, PORT, NUM_CONN)

try:
	while True:
		events = sel.select(timeout=1)
		for key, mask in events:
			service_conn(key, mask)
except KeyboardInterrupt:
	print("SIGINT caught, exiting")
finally:
	sel.close()
