import socket
import time
from threading import Thread
import query
from ctt import CTT, Packet, PacketType
import sys
sys.path.append('/Querys')
sys.path.append('/Parse')
from mensagem import DNS
from logs import endSessionLog, bootLog, writeLogLine
from infoBD import BD
IP = "127.0.0.3"  # ip do server ( tive de mudar o ip pq era desconhecido e o servidor nao corria
IP2 = "127.0.0.4"  # ip do ss
PORTA = 1222  # porta do server


class ServerWorker(Thread):

    def __init__(self, socket, address, servidor, type):
        self.socket = socket
        self.address = address
        self.servidor = servidor
        self.type = type

        Thread.__init__(self)

    def run(self):
        try:
            copia_bd = BD(self.servidor.DBDir)
            while True:
                if(self.type == "TCP"):
                    # Receber pacote da conexão
                    packet = CTT.recv_msg(self.socket)
                    # esta linha parece inutil  print(f"mensagem recebida de: {address}:{53}")
                    if packet != 'null':
                        # Processar pacote
                        # Caso a ligação seja feita com o SS e este peça uma cópia da BD
                        if packet.type == PacketType.GET_BD_REQUEST:
                            print(f"[SERVER WORKER] Recebi uma ligação do SS {IP2}")
                            num = 1#variavél para indicar as linhas que foram enviadas e recebidas
                            # enviar para o SS uma mensagem a confirmar inicio da transmissao da bd
                            numLinhas = copia_bd.numLinhas
                            CTT.send_msg(Packet(PacketType.NUM_LINHAS_BD, numLinhas),self.socket)
                            notificacao = CTT.recv_msg(self.socket)
                            if notificacao.type == PacketType.CONFIRM_NUM:
                                for linha in copia_bd.linhas:
                                    dados = (linha,num)
                                    CTT.send_msg(Packet(PacketType.BD_RESPONSE_LINE, dados),self.socket)  # enviar uma linha da BD
                                    num += 1
                                print(copia_bd)
                                print("[SERVER WORKER] Fim transferencia de zona")
                                writeLogLine(self.servidor, 'ZT', IP2,'')  # escrever no ficheiro de log que houve uma transferencia de zona
                if(self.type == "UDP"):
                    msg = self.socket[0] # a mensagem enviada pelo cliente
                    sck = self.socket[1] # o socket do servidor que irá responder a esta msg
                    # Caso o cliente envie uma mensagem
                    print(f"[SERVER WORKER] Recebi uma ligação do cliente {self.address}")
                    writeLogLine(self.servidor, 'QR', PORTA.__str__(), msg.data.debugLog())  # escrever no ficheiro de log que recebeu uma querie
                    value = query.answer(msg.data, copia_bd.linhas)  # processar a query recebida
                    CTT.send_msg_udp(Packet(PacketType.SERVER_RESPONSE, value), sck,self.address)  # enviar resposta a query para o cliente
                    print(msg.data.debug())
                    writeLogLine(self.servidor, 'QE', PORTA.__str__(),msg.data.debugLog())  # escrever no ficheiro de log que houve uma resposta a uma querie
                    break

        except KeyboardInterrupt:
            self.socket.close()
