import socket
import threading
import time


def main():
    ss_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # abrir socket
    IP2 = "127.0.0.4"  # ip da maquina
    IP = "127.0.0.3"
    FORMAT = 'utf-8'  # format de codificaçao
    PORTA = 100 # porta do server
    ss_server.bind((IP2, PORTA))  # dar bind ao ip e porta ao servidor
    ss_server.connect(("127.0.0.3", 53))  # connectar ao SP
    msg = 'get bd'
    ss_server.sendall(msg.encode(FORMAT))  # enviar o pedido para receber uma copia da BD do SP

    print(f"Estou à escuta no {IP2}:{PORTA}")
    print(f"Recebi uma ligação do SP {IP}")
    while True:
        msg = ss_server.recv(1024).decode(FORMAT)  # receber msg
        if msg == "bd_SP.txt":  # if para se a msg recebida for a resposta ao pedido de copia
            file = open("bd_SS.txt", "w")  # abrir ficheiro para guardar copia da BD do SP
            #data = ss_server.recv(1024).decode(FORMAT)  # receber os dados na BD do SP
            file.write(msg)  # escrever dados no ficheiro de texto aberto
            ss_server.send(f"File data received on SS".encode(FORMAT))  # enviar notificaçao para SP a verificar a receçao dos dados
            file.close()  # fechar ficheiro com a copia da BD
            print("copia da BD feita")
        if not msg:
            print("ligaçao acabou")
            break
        print(msg)
    ss_server.close()


if __name__ == "__main__":
    main()
