import socket
import sys
sys.path.append('/home/me/CC22-23/Parse')
from logs import endSessionLog, bootLog, writeLogLine
from infoServer import infoServer
from ctt import CTT, Packet, PacketType

IP2 = "127.0.0.4"  # ip da maquina
IP = "127.0.0.3"
PORTA = 2000  # porta do server
BD = []


def transf_zona(ss_server):
    # Enviar confirmação para o SP
    CTT.send_msg(Packet(PacketType.GET_BD_CONFIRM, None), ss_server)

    print(f"[SERVER SS] Estou à escuta no {IP2}:{PORTA}")
    print(f"[SERVER SS] Recebi uma ligação do SP {IP}")
    while True:
        # Receber pacote do SP
        packet = CTT.recv_msg(ss_server)
        if not packet:
            print("ligaçao acabou")
            break
        if packet.type == PacketType.GET_BD_END:
            CTT.send_msg(Packet(PacketType.GET_BD_CONFIRM_END, None), ss_server)
            print(f"[SERVER SS] Fim da transmissão de zona")
            print(BD)
            break
        if packet.type == PacketType.GET_BD_RESPONSE:
            CTT.send_msg(Packet(PacketType.GET_BD_CONFIRM, None), ss_server)
            BD.append(packet.data)


def main():
    ss_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # abrir socket
    ss_server.bind((IP2, PORTA))  # dar bind ao ip e porta ao servidor
    ss_server.connect(("127.0.0.3", 1222))  # connectar ao SP
    servidor = infoServer('/home/me/CC22-23/Parse/SPconfig.txt')#lẽ o ficheiro de configuraçao e cria uma classe com a informaçao do mesmo
    bootLog(servidor, PORTA, 2000)#dá inicio a este sessão no ficheiro de logs
    # Enviar o pedido para receber uma cópia da BD do SP
    CTT.send_msg(Packet(PacketType.GET_BD_REQUEST, None), ss_server)
    # Receber cópia da BD do SP
    transf_zona(ss_server)
    endSessionLog(servidor, PORTA.__str__())
    ss_server.close()


if __name__ == "__main__":
    main()
