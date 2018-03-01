
import socket

vinci = ("www.vinci.be",80)
s = socket.socket()         #TCP socket
s.connect(vinci)
s.send('GET / HTTP/1.0\n\n'.encode())
print(s.getsockname())
recieve = s.recv(512) .decode()      #512 = nbr octet max
print(recieve)