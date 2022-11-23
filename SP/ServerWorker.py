import socket
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
                        for linha in copia_bd.linhas:
                            CTT.send_msg(Packet(PacketType.GET_BD_RESPONSE, linha), self.socket)  # enviar uma linha da BD
                            notificacao = CTT.recv_msg(self.socket)  # ver se o ss recebe os dados
                            if notificacao.type != PacketType.GET_BD_CONFIRM:#caso o ss nao receba os dados
                                print("[SERVER WORKER] Erro na transmissão da BD linha: " + num.__str__())
                            num += 1
                        CTT.send_msg(Packet(PacketType.GET_BD_END, None), self.socket)  # confirmar o fim do envio da BD
                        notificacao = CTT.recv_msg(self.socket)  # verificar se o SS recebeu a copia corretamente
                        if notificacao.type == PacketType.GET_BD_CONFIRM_END:#confirmaçao que o ss recebeu a copia corretamente
                            print("[SERVER WORKER] Transmissão concluida")
                            writeLogLine(self.servidor, 'ZT', IP2, '')#escrever no ficheiro de log que houve uma transferencia de zona

                    # Caso o cliente se queira desconectar
                    elif packet.type == PacketType.CLIENT_DISCONNECT:
                        print("[SERVER WORKER] Ligação acabou")
                        break

                    # Caso o cliente envie uma mensagem
                    elif packet.type == PacketType.CLIENT_MESSAGE:
                        print(f"[SERVER WORKER] Recebi uma ligação do cliente {self.address}")
                        writeLogLine(self.servidor, 'QR', PORTA.__str__(), packet.data.debug() )#escrever no ficheiro de log que houve uma resposta a uma querie
                        value = query.answer(packet.data, copia_bd.linhas)#processar a query recebida
                        CTT.send_msg(Packet(PacketType.SERVER_RESPONSE, value), self.socket)#enviar resposta a query para o cliente

        except KeyboardInterrupt:
            self.socket.close()
