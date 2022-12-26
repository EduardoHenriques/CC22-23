import socket
from threading import Thread
from ctt import CTT
from ServerWorker import ServerWorker


class TCPListenSP(Thread):

    def __init__(self, porta, ip, servidor):
        self.porta = int(porta)
        self.ip = ip
        self.type = "TCP"
        self.servidor = servidor

        Thread.__init__(self)

    def run(self):
        try:
            sp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # criar socket
            sp_server.bind((self.ip, self.porta))  # dar bind ao ip e porta ao servidor
            sp_server.listen(5)  # servidor fica à espera de ligaçoes
            print(f"[SERVER] Estou à escuta no {self.ip}:{self.porta}")
            while True:
                connection, address = sp_server.accept()
                print("recebi uma ligaçao no TCP")
                worker = ServerWorker(connection, address, self.servidor, "TCP")
                worker.daemon = True
                worker.start()
                worker.join()
        # funcao para tratar de ligaçoes TCP
        except KeyboardInterrupt:
            print("yes")
