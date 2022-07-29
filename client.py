import socket

#temporarily hardcoded to localhost for sake of testing convenience
#HOST = input("Enter IP to connect to: ") 
HOST = "127.0.0.1"
PORT = 54321

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

mesg = input("Enter message to send: ").encode()
s.sendall(mesg)
data = s.recv(1024)

print(f"Response: {data.decode()}")
