import sys
from logs import endSessionLog, bootLog
from infoServer import infoServer
from TCP_SP import TCPListenSP
from UDPListen import UDPlisten


# IP = "127.0.0.3"  # ip do server ( tive de mudar o ip pq era desconhecido e o servidor nao corria
# IP2 = "127.0.0.4"  # ip do ss
# PORTA = 1222  # porta do server
# PORTA_UDP = 1223  # porta para coneccao UDP
# lẽ o ficheiro de configuraçao e cria uma classe com a informaçao do mesmo
# servidor = infoServer('/home/me/CC22-23/SP/caoSP_config.txt')


def main():
    args = sys.argv[1:]
    configPath = args[0]
    parsed = configPath.split('/')
    config = parsed[1].split('.')[0]
    nome = config.split('_')[0]
    IP = args[1]
    PORTA = args[2]
    PORTA_UDP = args[3]
    servidor = infoServer(configPath)
    try:
        ThreadUDP = UDPlisten(PORTA_UDP, IP, servidor, nome)
        ThreadTCP = TCPListenSP(PORTA, IP, servidor)
        print("Starting Server...")
        bootLog(servidor, PORTA, 2000)  # dá inicio a este sessão no ficheiro de logs
        bootLog(servidor, PORTA_UDP, 2000)
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
