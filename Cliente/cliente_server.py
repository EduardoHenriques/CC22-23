import socket
import cliente
import sys

sys.path.append('/home/me/CC22-23/Querys')
from mensagem import DNS

from ctt import CTT, Packet, PacketType

PORTA = 1223  # porta do server
# my_name = input("name: ")
# tipo_de_valor = input("tipo de valor: ")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # criar socket
sock.settimeout(3)
dados = input("inserir query:")
ADRESS = cliente.queryIP(dados)  # retirar o IP da query fornecida
query = cliente.querycliente(dados)  # funcçao que cria uma query
CTT.send_msg_udp(Packet(PacketType.CLIENT_MESSAGE, query), sock, ADRESS)  # enviar a query para o cliente
packet = CTT.recv_msg_udp(sock)  # receber resposta ao cliente
print(packet[0].data)  # dar print à resposta da query no terminal
sock.close()  # fechar socket
