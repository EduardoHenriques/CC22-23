import query
from ctt import CTT, Packet, PacketType
from dataField import data


def WorkerResolver(socket, addressCl, servidor):
    print("[RESOLVER]")
    msg = socket[0]
    print("NOME: " + msg.data.data.queryInfo[0])
    sck = socket[1]
    value = query.answer(msg.data, [], servidor, sck)
    if not value.data.respVals:
        print("[RESOLVER]nao havia valores na cache")
        adrServer = getServer(msg, servidor)  # vai buscar o DD da query em questao
        if not adrServer:  # se nao houver um servidor para este dominio
            print("[RESOLVER]nao havia DD para o dominio pedido")
            adrST = servidor.getST()  # vai buscar o servidor de topo
            print(adrST)
            for linha in adrST:
                print("[RESOLVER] tentar ligacao a ST")
                adrServer = linha.split(':')  # divide a linha para ter a porta e o ip do servidor
                # enviar a query para o SDT
                CTT.send_msg_udp(Packet(PacketType.SERVER_RESPONSE, msg.data), sck, (adrServer[0], int(adrServer[1])))
                try:
                    st_response = CTT.recv_msg_udp(sck)  # receber a resposta do ST
                    print("[RESOLVER] resposta recebida do ST")
                    for sdt_servers in st_response.data:
                        print("[RESOLVER] tentar ligacar a um SDT")
                        adr = getAdress(sdt_servers)
                        CTT.send_msg_udp(Packet(PacketType.SERVER_RESPONSE, msg.data), sck, adr)
                        try:
                            sdt_response = CTT.recv_msg_udp(sck)
                            print("[RESOLVER] resposta recebida do SDT")
                            for servers in sdt_response:
                                print("[RESOLVER] tentar ligacar a um Servidor")
                                adr = getAdress(servers)
                                CTT.send_msg_udp(Packet(PacketType.SERVER_RESPONSE, msg.data), sck, adr)
                                try:
                                    server_response = CTT.recv_msg_udp(sck)
                                    print("[RESOLVER] resposta recebida do SDT")
                                    if server_response.header.respCode == 0:
                                        print("[RESOLVER] Responder ao cliente")
                                        CTT.send_msg_udp(Packet(PacketType.SERVER_RESPONSE, server_response.data), sck,
                                                         addressCl)
                                        break
                                except sck.Timeout:
                                    print("tentar outro servidor")
                            break
                        except sck.Timeout:
                            print("tentar outro servidor")
                    break
                except sck.Timeout:
                    print("tentar outro sevidor")
        else:
            print(adrServer)
            conection = adrServer.split(':')

            CTT.send_msg_udp(Packet(PacketType.SERVER_RESPONSE, msg.data), sck, (conection[0], int(conection[1])))
            packet = CTT.recv_msg_udp(sck)
            msg = packet[0]
            print("[RESOLVER] resposta recebida do SERVIDOR")
            print(packet)
            print("[RESOLVER] Responder ao cliente")
            CTT.send_msg_udp(Packet(PacketType.SERVER_RESPONSE, msg.data), sck, addressCl)
    else:
        print("[RESOLVER] Responder ao cliente")
        CTT.send_msg_udp(Packet(PacketType.SERVER_RESPONSE, value), sck, addressCl)


def getServer(msg, servidor):
    lista = servidor.getDD()
    print("lista:")
    print(lista)
    if not lista:
        return None
    else:
        for linha in lista:
            if msg.data.data.queryInfo[0] in linha:
                print("LINHA:")
                print(linha)
                parsed = linha.split(' ')
                return parsed[2]
        return None


def getAdress(linha):
    parsed = linha.split(' ')
    (ip, porta) = parsed[3].split(':')
    par = (ip, porta)
    return par
