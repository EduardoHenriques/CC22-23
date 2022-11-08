import socket
import threading
import time


def main():

    sp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    FORMAT = 'utf-8'  # formato de codificaçao
    IP = "127.0.0.3"  # ip do server ( tive de mudar o ip pq era desconhecido e o servidor nao corria
    IP2 = "127.0.0.4" #ip do ss
    PORTA = 53  # porta do server
    sp_server.bind((IP, PORTA))  # dar bind ao ip e porta ao servidor
    sp_server.listen(5)  # servidor fica à espera de ligaçoes
    print(f"Estou à escuta no {IP}:{53}")
    connection, address = sp_server.accept()  # servidor aceita a ligaçao



    while True:

        msg = connection.recv(1024)  # servidor recebe uma mensagem
      # esta linha parece inutil  print(f"mensagem recebida de: {address}:{53}")
        if address[0] == IP2:  # caso a ligaçao feita seja com o SS  - Este ciclo esta a mandar 6x a msg para o ss
            print(f"Recebi uma ligação do SP {IP2}")
            file = open("bd_SP.txt", "r")  # abrir o ficheiro onde tem a BD
            copia_bd = file.read()  # ler a BD
            # enviar para o SS uma mensagem a confirmar inicio da transmissao da bd
            connection.sendall("bd_SP.txt".encode(FORMAT))
            connection.sendall(copia_bd.encode(FORMAT))  # enviar uma copia da BD
            notificacao = connection.recv(1024).decode(FORMAT) # ver se o ss recebe os dados
            print (notificacao)
        elif not msg:
            print("ligaçao acabou")
            break
        else:
            print(f"Recebi uma ligação do cliente {address}")
            print(msg.decode('utf-8'))
            msg = 'mensagem recebida no servidor'
            connection.sendall(msg.encode('utf-8'))
    sp_server.close()


if __name__ == "__main__":
    main()



#