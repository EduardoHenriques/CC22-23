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
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#criar socket
sock.connect((IP, PORTA))#conectar socket ao SP
query = cliente.querycliente()#funcçao que cria uma query
CTT.send_msg(Packet(PacketType.CLIENT_MESSAGE, query), sock)#enviar a query para o cliente
packet = CTT.recv_msg(sock)#receber resposta ao cliente
print(packet.data)#dar print à resposta da query no terminal
CTT.send_msg(Packet(PacketType.CLIENT_DISCONNECT, query), sock)#enviar ao servidor pedido para fechar conexao
sock.close()#fechar socket
