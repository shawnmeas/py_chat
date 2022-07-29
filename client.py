import socket

HOST = input("Enter IP to connect to: ") 
PORT = 54321

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(b"Test")
data = s.recv(1024)

print(f"Response: {data}")
