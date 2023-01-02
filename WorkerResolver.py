import query
from ctt import CTT, Packet, PacketType


def WorkerResolver(socket, addressCl, servidor):
    print("[RESOLVER]")
    msg = socket[0]
    sck = socket[1]
    value = query.answer(msg.data, [], servidor, sck, "")
    if not value.data.respVals:
        print("[RESOLVER]nao havia valores na cache")
        adrServer = getServer(msg, servidor)  # vai buscar o DD da query em questao
        if not adrServer:  # se nao houver um servidor para este dominio
            print("[RESOLVER]nao havia DD para o dominio pedido")
            adrST = servidor.getST()  # vai buscar o servidor de topo
            for linha in adrST:
                print("[RESOLVER] tentar ligacao a ST")
                adrServer = linha.split(':')  # divide a linha para ter a porta e o ip do servidor
                # enviar a query para o SDT
                CTT.send_msg_udp(Packet(PacketType.SERVER_RESPONSE, msg.data), sck, (adrServer[0], int(adrServer[1])))
                try:
                    # receber a resposta do ST com a lista de todos os SDT disponiveis
                    st_response = CTT.recv_msg_udp(sck)
                    print("[RESOLVER] resposta recebida do ST")
                    for sdt_servers in st_response[0].data.data.extraVals:  # para cada linha recebido
                        print("[RESOLVER] tentar ligacar a um SDT")
                        adr = getAdress(sdt_servers)  # ir buscar o par ip:porta do SDT a linha
                        # enviar para o SDT a query
                        CTT.send_msg_udp(Packet(PacketType.SERVER_RESPONSE, msg.data), sck, adr)
                        try:
                            # receber a resposta do SDT com a lista de todos os servidores disponiveis
                            sdt_response = CTT.recv_msg_udp(sck)
                            print("[RESOLVER] resposta recebida do SDT")
                            # SDT nao encontrou valores correspondentes ao nome da query
                            if sdt_response[0].data.header.respCode == "1":
                                # como nao havia o nome da query envia o codigo de erro 2
                                sdt_response[0].data.header.respCode = "2"
                                sdt_response[0].data.header.flags = changeFlags(sdt_response[0].data)
                                servidor.BD_e_Cache.query_to_cache(sdt_response[0].data, "resolver")
                                print('\n' + msg.data.debug())
                                CTT.send_msg_udp(Packet(PacketType.SERVER_RESPONSE, sdt_response[0].data), sck, addressCl)
                                break
                            else:
                                for servers in sdt_response[0].data.data.extraVals:  # para cada linha recebido
                                    print("[RESOLVER] tentar ligacar a um Servidor")
                                    adr = getAdress(servers)
                                    CTT.send_msg_udp(Packet(PacketType.SERVER_RESPONSE, msg.data), sck, adr)
                                    try:
                                        server_response = CTT.recv_msg_udp(sck)
                                        print("[RESOLVER] resposta recebida do Servidor")
                                        server_response[0].data.header.flags = changeFlags(server_response[0].data)
                                        print("[RESOLVER] Responder ao cliente")
                                        servidor.BD_e_Cache.query_to_cache(server_response[0].data, "resolver")
                                        print('\n' + msg.data.debug())
                                        CTT.send_msg_udp(Packet(PacketType.SERVER_RESPONSE, server_response[0].data),
                                                         sck, addressCl)
                                        break
                                    except sck.timeout:
                                        print("tentar outro servidor")
                                break
                        except sck.timeout:
                            print("tentar outro servidor")
                    break
                except sck.timeout:
                    print("tentar outro sevidor")
        else:
            conection = adrServer.split(':')
            CTT.send_msg_udp(Packet(PacketType.SERVER_RESPONSE, msg.data), sck, (conection[0], int(conection[1])))
            packet = CTT.recv_msg_udp(sck)
            msg = packet[0]
            print("[RESOLVER] resposta recebida do SERVIDOR")
            print("[RESOLVER] Responder ao cliente")
            msg.data.header.flags = changeFlags(msg.data)
            servidor.BD_e_Cache.query_to_cache(msg.data, "resolver")
            print('\n' + msg.data.debug())
            CTT.send_msg_udp(Packet(PacketType.SERVER_RESPONSE, msg.data), sck, addressCl)
    else:
        print("[RESOLVER] Responder ao cliente")
        value.data.header.flags = changeFlags(value)
        servidor.BD_e_Cache.query_to_cache(value, "resolver")
        print('\n' + msg.data.debug())
        CTT.send_msg_udp(Packet(PacketType.SERVER_RESPONSE, value), sck, addressCl)


# funcao que verifica se existe o dominio pedido na query no ficheiro de config do resolver
def getServer(msg, servidor):
    lista = servidor.getDD()  # lista com todos os DD no ficheiro de config
    if not lista:
        return None
    else:
        for linha in lista:
            parsed = linha.split(' ')
            nome = parsed[0]
            if msg.data.data.queryInfo[0] == nome:
                  # retirar o ip da linha em questao
                return parsed[2]  # devolver o ip
        return None  # caso nenhum dos DD coincida com o nome pedido na query


# retirar A das flags uma vez que servidores resolver nunca vao ser autoritativos
def changeFlags(msg):
    flags = msg.header.flags
    new = flags.replace("+A", "")
    if "A" in new:
        new_new = new.replace("A", "")
        return new_new
    return new
def getAdress(linha):
    parsed = linha.split(' ')
    (ip, porta) = parsed[2].split(':')
    par = (ip, int(porta))
    return par
