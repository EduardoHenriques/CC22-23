import socket
from threading import Thread
from ctt import CTT
from ServerWorker import ServerWorker


class UDPlisten(Thread):

    def __init__(self, porta, ip, servidor):
        self.porta = porta
        self.ip = ip
        self.type = "UDP"
        self.servidor = servidor

        Thread.__init__(self)

    def run(self):
        try:
            sp_serverUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # criar socket UDP
            sp_serverUDP.bind((self.ip, self.porta))  # dar bind ao ao ip e porta ao servidor
            print(f"[SERVER] Estou à escuta no {self.ip}:{self.porta}")
            while True:
                msg, address_UDP = CTT.recv_msg_udp(sp_serverUDP)
                print("recebi uma ligaçao no UDP")
                workerUDP = ServerWorker((msg, sp_serverUDP), address_UDP, self.servidor, self.type)
                workerUDP.daemon = True
                workerUDP.start()
        except KeyboardInterrupt:
            print("yes")
