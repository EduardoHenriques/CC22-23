import socket

from SP.ServerWorker import ServerWorker
from enum import Enum


IP = "127.0.0.3"  # ip do server ( tive de mudar o ip pq era desconhecido e o servidor nao corria
IP2 = "127.0.0.4"  # ip do ss
PORTA = 53  # porta do server


def main():
    # Inicializar o servidor
    sp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sp_server.bind((IP, PORTA))  # dar bind ao ip e porta ao servidor
    sp_server.listen(5)  # servidor fica à espera de ligaçoes
    print(f"[SERVER] Estou à escuta no {IP}:{53}")

    try:
        while True:
            # Esperar por uma conexão
            connection, address = sp_server.accept()
            print(f"[SERVER] Conexão aceite. {address}")

            # Criar thread responsável por esta conexão
            worker = ServerWorker(connection, address)
            worker.daemon = True
            worker.start()

    except KeyboardInterrupt:
        print("[SERVER] Servidor interrompido!")

    sp_server.close()


if __name__ == "__main__":
    main()

#
