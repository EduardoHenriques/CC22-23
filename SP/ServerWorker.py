import socket
import time
from threading import Thread
import query
from ctt import CTT, Packet, PacketType
import sys
sys.path.append('/home/me/CC22-23/Querys')
sys.path.append('/home/me/CC22-23/Parse')
from mensagem import DNS
from logs import endSessionLog, bootLog, writeLogLine
from infoBD import BD
IP = "127.0.0.3"  # ip do server ( tive de mudar o ip pq era desconhecido e o servidor nao corria
IP2 = "127.0.0.4"  # ip do ss
PORTA = 1222  # porta do server


class ServerWorker(Thread):

    def __init__(self, socket, address, servidor):
        self.socket = socket
        self.address = address
        self.servidor = servidor

        Thread.__init__(self)

    def run(self):
        try:
            copia_bd = BD(self.servidor.DBDir)
            while True:
                # Receber pacote da conexão
                packet = CTT.recv_msg(self.socket)
                # esta linha parece inutil  print(f"mensagem recebida de: {address}:{53}")
                if packet != 'null':
                    # Processar pacote
                    # Caso a ligação seja feita com o SS e este peça uma cópia da BD
                    if self.address[0] == IP2 and packet.type == PacketType.GET_BD_REQUEST:
                        print(f"[SERVER WORKER] Recebi uma ligação do SS {IP2}")
                        file = open("bd_SP.txt", "r")  # abrir o ficheiro onde tem a BD
                        num = 1#variavél para indicar as linhas que foram enviadas e recebidas
                        # enviar para o SS uma mensagem a confirmar inicio da transmissao da bd
                        numLinhas = copia_bd.numLinhas
                        CTT.send_msg(Packet(PacketType.NUM_LINHAS_BD, numLinhas),self.socket)
                        notificacao = CTT.recv_msg(self.socket)
                        if notificacao.type == PacketType.CONFIRM_NUM:
                            for linha in copia_bd.linhas:
                                dados = (linha,num)
                                CTT.send_msg(Packet(PacketType.BD_RESPONSE_LINE, dados),
                                             self.socket)  # enviar uma linha da BD
                                num += 1
                            print(copia_bd)
                            writeLogLine(self.servidor, 'ZT', IP2,'')  # escrever no ficheiro de log que houve uma transferencia de zona
                    # Caso o cliente se queira desconectar
                    elif packet.type == PacketType.CLIENT_DISCONNECT:
                        print("[SERVER WORKER] Ligação acabou")
                        break

                    # Caso o cliente envie uma mensagem
                    elif packet.type == PacketType.CLIENT_MESSAGE:
                        print(f"[SERVER WORKER] Recebi uma ligação do cliente {self.address}")
                        writeLogLine(self.servidor, 'QR', PORTA.__str__(), packet.data.debugLog() )#escrever no ficheiro de log que recebeu uma querie
                        value = query.answer(packet.data, copia_bd.linhas)#processar a query recebida
                        CTT.send_msg(Packet(PacketType.SERVER_RESPONSE, value), self.socket)#enviar resposta a query para o cliente
                        print(packet.data.debug())
                        writeLogLine(self.servidor, 'QE', PORTA.__str__(),packet.data.debugLog())  # escrever no ficheiro de log que houve uma resposta a uma querie

        except KeyboardInterrupt:
            self.socket.close()
