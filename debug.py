import socket


addr = ('127.0.0.1',5094)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(addr)
s.sendall('hello,world')
s.close()