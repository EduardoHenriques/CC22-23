import socket
from threading import Thread
import sys
from ctt import CTT

sys.path.append('/home/me/CC22-23/Parse')
sys.path.append('/home/me/CC22-23/Querys')
from logs import endSessionLog, bootLog
from infoServer import infoServer
from TCP_SP import TCPListen
from UDPListen import UDPlisten
from ServerWorker import ServerWorker

IP = "127.0.0.3"  # ip do server ( tive de mudar o ip pq era desconhecido e o servidor nao corria
IP2 = "127.0.0.4"  # ip do ss
PORTA = 1222  # porta do server
PORTA_UDP = 1223  # porta para coneccao UDP
# lẽ o ficheiro de configuraçao e cria uma classe com a informaçao do mesmo
servidor = infoServer('/home/me/CC22-23/SP/caoSP_config.txt')


def main():
    try:
        ThreadUDP = UDPlisten(PORTA_UDP, IP, servidor)
        ThreadTCP = TCPListen(PORTA, IP, servidor)
        print("Starting Server...")
        bootLog(servidor, PORTA, 2000)  # dá inicio a este sessão no ficheiro de logs
        bootLog(servidor, PORTA_UDP, 2000)
        ThreadUDP.daemon = True
        ThreadUDP.start()
        ThreadTCP.start()
        print("Server Started!")
        ThreadUDP.join()
        ThreadTCP.join()

    except KeyboardInterrupt:
        print("[SERVER] Servidor interrompido!")
        endSessionLog(servidor, PORTA.__str__())
        endSessionLog(servidor, PORTA_UDP.__str__())


if __name__ == "__main__":
    main()
