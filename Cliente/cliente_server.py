import socket
import cliente
import sys
sys.path.append('/home/me/CC22-23/Querys')
from mensagem import DNS

from ctt import CTT, Packet, PacketType

IP = "127.0.0.3"  # ip do server
PORTA = 1222  # porta do server
#my_name = input("name: ")
#tipo_de_valor = input("tipo de valor: ")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, PORTA))
#s.setblocking(1)

query = cliente.querycliente()
CTT.send_msg(Packet(PacketType.CLIENT_MESSAGE, query), sock)
packet = CTT.recv_msg(sock)
print(packet.data)
msh = ''
CTT.send_msg(Packet(PacketType.CLIENT_DISCONNECT, query), sock)
sock.close()
