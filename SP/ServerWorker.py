from threading import Thread
from ctt import CTT, Packet, PacketType

IP = "127.0.0.3"  # ip do server ( tive de mudar o ip pq era desconhecido e o servidor nao corria
IP2 = "127.0.0.4"  # ip do ss
PORTA = 53  # porta do server


class ServerWorker(Thread):

    def __init__(self, socket, address):
        self.socket = socket
        self.address = address

        Thread.__init__(self)

    def run(self):

        try:
            while True:
                # Receber pacote da conexão
                packet = CTT.recv_msg(self.socket)
                # esta linha parece inutil  print(f"mensagem recebida de: {address}:{53}")

                # Processar pacote
                # Caso a ligação seja feita com o SS e este peça uma cópia da BD
                if self.address[0] == IP2 and packet.type == PacketType.GET_BD_REQUEST:
                    print(f"[SERVER WORKER] Recebi uma ligação do SP {IP2}")
                    file = open("bd_SP.txt", "r")  # abrir o ficheiro onde tem a BD
                    copia_bd = file.read()  # ler a BD
                    # enviar para o SS uma mensagem a confirmar inicio da transmissao da bd
                    CTT.send_msg(Packet(PacketType.GET_BD_RESPONSE, copia_bd), self.socket)  # enviar uma copia da BD
                    notificacao = CTT.recv_msg(self.socket)  # ver se o ss recebe os dados
                    if notificacao.type != PacketType.GET_BD_CONFIRM:
                        print("[SERVER WORKER] Erro na transmissão da BD.")

                # Caso o cliente se queira desconectar
                elif packet.type == PacketType.CLIENT_DISCONNECT:
                    print("[SERVER WORKER] Ligação acabou")
                    break

                # Caso o cliente envie uma mensagem
                elif packet.type == PacketType.CLIENT_MESSAGE:
                    print(f"[SERVER WORKER] Recebi uma ligação do cliente {self.address}")
                    print(packet.data)
                    msg = 'mensagem recebida no servidor'
                    CTT.send_msg(Packet(PacketType.SERVER_RESPONSE, msg), self.socket)

        except KeyboardInterrupt:
            self.socket.close()
