import socket
from WorkerResolver import WorkerResolver
from ctt import CTT
import sys
sys.path.append('/Parse')
from logs import endSessionLog, bootLog
from infoServer import infoServer
# IP = "127.0.0.5"
# PORTA_UDP = 3000
BUFFER_SIZE = 1024

def main():
    args = sys.argv[1:]
    configPath = args[0]
    IP = args[1]
    PORTA_UDP = int(args[2])
    servidor = infoServer(configPath)
    try:
        socketResolver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # criar socket UDP
        socketResolver.bind((IP, PORTA_UDP))  # dar bind ao ao ip e porta ao servidor
        print(f"[SERVER] Estou à escuta no {IP}:{PORTA_UDP}")
        while True:
            msg, addressCl = CTT.recv_msg_udp(socketResolver)
            print("recebi uma ligaçao no UDP")
            WorkerResolver((msg, socketResolver), addressCl, servidor)

    except KeyboardInterrupt:
        print("[SERVER] Servidor interrompido!")
        endSessionLog(servidor, PORTA_UDP.__str__())

if __name__ == "__main__":
    main()
