import socket
import threading
import time


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 53))
    s.listen()

    print(f"Estou à escuta no {socket.gethostname()}:{53}")

    while True:
        connection, address = s.accept()
        msg = connection.recv(1024)

        if not msg:
            print("liagaçao acabou")
            break
        print(msg.decode('utf-8'))
        msg = 'mensagem recebida no servidor'
        print(f"Recebi uma ligação do cliente {address}")
        connection.sendall(msg.encode('utf-8'))
    s.close()


if __name__ == "__main__":
    main()
