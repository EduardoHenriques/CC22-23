import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 53))

s.sendall(input().encode('utf-8'))
print("msg enviada para servidor")
print("à espera")
msg = s.recv(1024)
print(msg.decode('utf-8'))
# time.sleep(1)
s.close()
