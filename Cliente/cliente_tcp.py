import socket
import sys
import time
import cliente
import pickle
HEADER_LENGTH = 10
IP = socket.gethostname()  # ip do server
PORTA = 53  # porta do server
#my_name = input("name: ")
#tipo_de_valor = input("tipo de valor: ")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORTA))
msg = cliente.querycliente()
s.sendall(msg)
print("msg enviada para servidor")
print("à espera")
msg = s.recv(1024)
print((pickle.loads(msg)))

s.close()
