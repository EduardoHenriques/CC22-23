import socket

from infoBD import linhaBD_to_linhaCache
from ctt import CTT, Packet, PacketType


def transf_zona(ss_server, IP2, PORTA, info):
    # Enviar o pedido para receber uma cópia da BD do SP
    CTT.send_msg(Packet(PacketType.GET_BD_REQUEST, None), ss_server)
    # Enviar confirmação para o SP
    print(f"[SERVER SS] Estou à escuta no {IP2}:{PORTA}")
    try:
        packet = CTT.recv_msg(ss_server)
        print(f"[SERVER SS] Recebi uma ligação do SP")
        # Receber pacote do SP
    except socket.timeout:
        print(f"[SERVER SS] Erro na transmissão de zona")
        return False
    if not packet:
        print("ligaçao acabou")
        return False
    if packet.type == PacketType.NUM_LINHAS_BD:
        num = packet.data
        CTT.send_msg(Packet(PacketType.CONFIRM_NUM, None), ss_server)
        i = 0
        while i < num:
            try:
                packet = CTT.recv_msg(ss_server)
            except socket.timeout:
                print(f"[SERVER SS] Erro na transmissão de zona")
                return False
            i = i + 1
            if packet.type == PacketType.BD_RESPONSE_LINE:
                info.BD_e_Cache.cache.inserirCache(linhaBD_to_linhaCache(packet.data[0], "SP"))
                if i == num:
                    print(f"[SERVER SS] Fim da transmissão de zona")
                    info.BD_e_Cache.cache.showCache()
                    return True
