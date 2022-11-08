import socket
import sys
import time
HEADER_LENGTH = 10
IP = "127.0.0.3"  # ip do server
PORTA = 53  # porta do server
my_name = input("name: ")
tipo_de_valor = input("tipo de valor: ")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORTA))
s.setblocking(1)

#s.sendall(input().encode('utf-8'))
#print("msg enviada para servidor")
#print("à espera")

#while True:
#   msg = s.recv(1024)
#   print(msg.decode('utf-8'))
# time.sleep(1)
 #  s.close()
name = my_name.encode('utf-8')
name_header = f"{len(name):<{HEADER_LENGTH}}".encode('utf-8')
s.send(name_header + name)



tipo = tipo_de_valor.encode('utf-8')
tipo_header = f"{len(tipo):<{HEADER_LENGTH}}".encode('utf-8')
s.send(tipo_header + tipo)



while True:
    tipo = input(f'{my_name} > ')
    if tipo:
       # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
       tipo = tipo_de_valor.encode('utf-8')
       tipo_header = f"{len(tipo):<{HEADER_LENGTH}}".encode('utf-8')
       s.send(tipo_header + tipo)

       while True:

          name_header = s.recv(HEADER_LENGTH)

          # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
          if not len(name_header):
             print('Connection closed by the server')
             sys.exit()
             # Convert header to int value
             name_length = int(name_header.decode('utf-8').strip())

             # Receive and decode username
             name = s.recv(name_length).decode('utf-8')

             # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
             tipo_header = s.recv(HEADER_LENGTH)
             tipo_length = int(tipo_header.decode('utf-8').strip())
             tipo = s.recv(tipo_length).decode('utf-8')

             # Print message
             print(f'{name} > {message}')