import socket
import sys
import time
HEADER_LENGTH = 10
IP = "127.0.0.3"  # ip do server
PORTA = 53  # porta do server
#my_name = input("name: ")
#tipo_de_valor = input("tipo de valor: ")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORTA))
s.setblocking(1)

s.sendall(input("name: " + "tipo de valor: ").encode('utf-8'))
print("msg enviada para servidor")
print("à espera")

while True:
   msg = s.recv(1024)
   print(msg.decode('utf-8'))
   time.sleep(1)
   s.close()
