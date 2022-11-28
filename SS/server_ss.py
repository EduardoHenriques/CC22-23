import socket
import sys
import time
from datetime import datetime

sys.path.append('/home/me/CC22-23/Parse')
from logs import endSessionLog, bootLog, writeLogLine
from infoServer import infoServer
from ctt import CTT, Packet, PacketType

IP2 = "127.0.0.4"  # ip da maquina
IP = "127.0.0.3"
PORTA = 2000  # porta do server
BD = []


def transf_zona(ss_server):
    # Enviar o pedido para receber uma cópia da BD do SP
    CTT.send_msg(Packet(PacketType.GET_BD_REQUEST, None), ss_server)
    # Enviar confirmação para o SP
    print(f"[SERVER SS] Estou à escuta no {IP2}:{PORTA}")
    print(f"[SERVER SS] Recebi uma ligação do SP {IP}")
    # Receber pacote do SP
    try:
        packet = CTT.recv_msg(ss_server)
    except socket.timeout:
        print(f"[SERVER SS] Erro na transmissão de zona")
        return False
    if not packet:
        print("ligaçao acabou")
        return False
    if packet.type == PacketType.NUM_LINHAS_BD:
        num = packet.data
        print(num)
        CTT.send_msg(Packet(PacketType.CONFIRM_NUM, None), ss_server)
        i = 0
        while i < num:
            try:
                packet = CTT.recv_msg(ss_server)
            except socket.timeout:
                print(f"[SERVER SS] Erro na transmissão de zona")
                return False
            i = i + 1
            if i == num:
                print(f"[SERVER SS] Fim da transmissão de zona")
                BD.append(packet.data)
                for linha in BD:
                    print(linha)
                return True
            if packet.type == PacketType.BD_RESPONSE_LINE:
                print("data:")
                print(packet.data)
                BD.append(packet.data)


def main():
    ss_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # abrir socket
    ss_server.bind((IP2, PORTA))  # dar bind ao ip e porta ao servidor
    ss_server.settimeout(5)
    ss_server.connect(("127.0.0.3", 1222))  # connectar ao SP
    servidor = infoServer('/home/me/CC22-23/Parse/SPconfig.txt')#lẽ o ficheiro de configuraçao e cria uma classe com a informaçao do mesmo
    bootLog(servidor, PORTA, 2000)#dá inicio a este sessão no ficheiro de logs
    # Receber cópia da BD do SP
    t = True
    counter = 0
    while t and counter != 3:
        counter = counter + 1
        t = not transf_zona(ss_server)
        if t:
            print(f"[SERVER SS] Tentar outra vez...")
            time.sleep(3)
    if t and counter == 3:
        print(f"[SERVER SS] Ligacao falhou")
    endSessionLog(servidor, PORTA.__str__())
    ss_server.close()


if __name__ == "__main__":
    main()
