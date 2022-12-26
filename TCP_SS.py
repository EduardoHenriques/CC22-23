import socket
import time
from threading import Thread

from Trasnf_zona import transf_zona
from ServerWorker import ServerWorker


class TCPListenSS(Thread):

    def __init__(self, porta, ip, ip_SP,servidor, BD):
        self.porta = int(porta)
        self.ip = ip
        self.ip_SP = ip_SP
        self.type = "TCP"
        self.servidor = servidor
        self.BD = BD

        Thread.__init__(self)

    def run(self):
        try:
            ss_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # criar socket
            ss_server.bind((self.ip, self.porta))  # dar bind ao ip e porta ao servidor
            ss_server.settimeout(5)  # colocar o timeout a 5
            ss_server.connect((self.ip_SP, 1222))  # connectar ao SP
            # Receber cópia da BD do SP
            t = True
            counter = 0
            while t and counter != 3:
                counter = counter + 1
                t = not transf_zona(ss_server, self.ip, self.porta, self.servidor)
                if t:
                    print(f"[SERVER SS] Tentar outra vez...")
                    time.sleep(3)
            if t and counter == 3:
                print(f"[SERVER SS] Ligacao falhou")
            print(f"[SERVER] Estou à escuta no {self.ip}:{self.porta}")
        # funcao para tratar de ligaçoes TCP
        except KeyboardInterrupt:
            print("yes")
