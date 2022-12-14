import socket
import sys
import threading
import time
from datetime import datetime
from threading import Thread

sys.path.append('/home/me/CC22-23/Parse')

from logs import endSessionLog, bootLog, writeLogLine
from infoServer import infoServer
from ctt import CTT, Packet, PacketType
from ServerWorker import ServerWorker
from UDPListen import UDPlisten
from TCP_SS import TCPListen

IP2 = "127.0.0.4"  # ip da maquina
IP = "127.0.0.3"
PORTA = 2000  # porta do server
PORTA_UDP = 2001
BD = []
BUFFER_SIZE = 1024
servidor = infoServer('/home/me/CC22-23/SS/caoSS1_config.txt')  # lẽ o ficheiro de configuraçao e cria uma classe com a informaçao do mesmo
servidor.showInfo()
def main():
    try:
        ThreadUDP = UDPlisten(PORTA_UDP, IP2, servidor)
        ThreadTCP = TCPListen(PORTA, IP2, IP, servidor, BD)
        bootLog(servidor, PORTA, 2000)  # dá inicio a este sessão no ficheiro de logs
        print("Starting Server...")
        ThreadUDP.start()
        ThreadTCP.start()
        print("Server Started!")
        ThreadUDP.join()
        ThreadTCP.join()

    except KeyboardInterrupt:
        print("[SERVER] Servidor interrompido!")
        endSessionLog(servidor, PORTA.__str__())


if __name__ == "__main__":
    main()
