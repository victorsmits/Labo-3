
import socket

vinci = ("www.vinci.be",80)
s = socket.socket()
s.connect(vinci)
s.send('GET /shit HTTP/1.0\n\n'.encode())
print(s.getsockname())
recieve = s.recvfrom(512)
print(recieve)