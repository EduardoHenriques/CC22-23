import socket
import sys
sys.path.append('/home/me/CC22-23/Parse')
sys.path.append('/home/me/CC22-23/Querys')
from logs import endSessionLog, bootLog, writeLogLine
from SP.ServerWorker import ServerWorker
from infoServer import infoServer
from enum import Enum

IP = "127.0.0.3"  # ip do server ( tive de mudar o ip pq era desconhecido e o servidor nao corria
IP2 = "127.0.0.4"  # ip do ss
PORTA = 1222  # porta do server


def main():
    # Inicializar o servidor
    sp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #criar socket
    sp_server.bind((IP, PORTA))  # dar bind ao ip e porta ao servidor
    sp_server.listen(5)  # servidor fica à espera de ligaçoes
    print(f"[SERVER] Estou à escuta no {IP}:{53}")
    servidor = infoServer('/home/me/CC22-23/Parse/SPconfig.txt') #lẽ o ficheiro de configuraçao e cria uma classe com a informaçao do mesmo
    bootLog(servidor, PORTA, 2000)#dá inicio a este sessão no ficheiro de logs
    try:
        while True:
            # Esperar por uma conexão
            connection, address = sp_server.accept()
            print(f"[SERVER] Conexão aceite. {connection}")
            # Criar thread responsável por esta conexão
            worker = ServerWorker(connection, address, servidor)
            worker.daemon = True
            worker.start()

    except KeyboardInterrupt:
        print("[SERVER] Servidor interrompido!")
        endSessionLog(servidor, PORTA.__str__())
        sp_server.close()

    sp_server.close()


if __name__ == "__main__":
    main()
