import socket

from ctt import CTT, Packet, PacketType

IP = "127.0.0.3"  # ip do server
PORTA = 53  # porta do server
#my_name = input("name: ")
#tipo_de_valor = input("tipo de valor: ")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, PORTA))
#s.setblocking(1)

name = input("Name: ")
type_of_value = input("Type of value: ")

CTT.send_msg(Packet(PacketType.CLIENT_DISCONNECT, None), sock)

sock.close()
