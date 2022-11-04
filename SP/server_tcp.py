import socket
import threading
import time


def main():
    sp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    FORMAT = 'utf-8'  # formato de codificaçao
    IP = "192.168.1.16"  # ip do server
    PORTA = 53  # porta do server
    sp_server.bind((IP, PORTA))  # dar bind ao ip e porta ao servidor
    sp_server.listen()  # servidor fica à espera de ligaçoes
    print(f"Estou à escuta no {IP}:{53}")

    while True:
        connection, address = sp_server.accept()  # servidor aceita a ligaçao
        msg = connection.recv(1024)  # servidor recebe uma mensagem
        print(msg)
        print(f"mensagem recebida de: {address}:{53}")
        if address[0] == IP:  # caso a ligaçao feita seja com o SS
            file = open("bd_SP.txt", "r")  # abrir o ficheiro onde tem a BD
            copia_bd = file.read()  # ler a BD
            # enviar para o SS uma mensagem a confirmar inicio da transmissao da bd
            connection.sendall("bd_SP.txt".encode(FORMAT))
            connection.sendall(copia_bd.encode(FORMAT))  # enviar uma copia da BD
        elif not msg:
            print("liagaçao acabou")
            break
        else:
            print(msg.decode('utf-8'))
            msg = 'mensagem recebida no servidor'
            print(f"Recebi uma ligação do cliente {address}")
            connection.sendall(msg.encode('utf-8'))
    sp_server.close()


if __name__ == "__main__":
    main()
