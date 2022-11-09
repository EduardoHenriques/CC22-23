import socket

from ctt import CTT, Packet, PacketType

IP2 = "127.0.0.4"  # ip da maquina
IP = "127.0.0.3"
PORTA = 100  # porta do server


def main():
    ss_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # abrir socket
    ss_server.bind((IP2, PORTA))  # dar bind ao ip e porta ao servidor
    ss_server.connect(("127.0.0.3", 53))  # connectar ao SP

    # Enviar o pedido para receber uma cópia da BD do SP
    CTT.send_msg(Packet(PacketType.GET_BD_REQUEST, None), ss_server)

    # Receber cópia da BD do SP
    packet = CTT.recv_msg(ss_server)
    file = open("bd_SS.txt", "w")
    file.write(packet.data)
    file.close()

    # Enviar confirmação para o SP
    CTT.send_msg(Packet(PacketType.GET_BD_CONFIRM, None), ss_server)

    print(f"[SERVER SS] Estou à escuta no {IP2}:{PORTA}")
    print(f"[SERVER SS] Recebi uma ligação do SP {IP}")

    try:
        while True:
            # Receber pacote do SP
            packet = CTT.recv_msg(ss_server)

            if not packet:
                print("ligaçao acabou")
                break
            print(packet)

    except KeyboardInterrupt:
        ss_server.close()


if __name__ == "__main__":
    main()
