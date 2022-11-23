import sys
sys.path.append('/home/me/CC22-23/Querys')
from mensagem import DNS


def get_default(nome, linhas):
    for linha in linhas:
        if nome in linha and 'DEFAULT' in linha:
            values = linha.split(' ')
            nome = values[0]
    return nome


def verifica_extras(valor_res, valor_aut, linha):
    fstlinha = linha.split(' ')[0]
    for res in valor_res:
        nome_ext = res.split(' ')[2]
        nome = nome_ext.split('.')[0]
        if nome == fstlinha:
            return True
    for res in valor_aut:
        nome_ext = res.split(' ')[2]
        nome = nome_ext.split('.')[0]
        if nome == fstlinha:
            return True
    return False


def answer(DNS_query, bd):
    nome = DNS_query.data.queryInfo[0]#campo nome do header DNS
    tipo = DNS_query.data.queryInfo[1]#campo tipo do header DNS
    flags = DNS_query.header.flags#campo flags do header DNS
    valor_res = []#campo valor de resposta do header DNS
    valor_aut = []#campo valores autoritaticos do header DNS
    valor_ext = []#campo valores extra do header DNS
    nome = get_default(nome, bd)#funçao que associa um carater ao valor de DEFAULT na base de dados
    for linha in bd:
        fstelem = linha.split(' ')[0]#1ª palavra de em cada linha da BD
        if nome == fstelem and tipo in linha:#verificar se a linha contem o nome e o tipo da query recebida
            valor_res.append(linha[:-1])#se sim adiciona a linha ao campo de valores de reposta
        if nome == fstelem and 'NS' in linha:#verifica se a linha contem valores autoritativos
            valor_aut.append(linha[:-1])#se sim adiciona a linha ao campo de valores autoritativos
        if 'A' in linha:#verificar se linhas correspondem a campos extra
            if verifica_extras(valor_res, valor_aut, linha):#verifica se algum dos campos pedidos na query estao nes
                valor_ext.append(linha[:-1])
    DNS_query.data.respVals = valor_res
    DNS_query.data.auhtorityVals = valor_aut
    DNS_query.data.extraVals = valor_ext
    DNS_query.header.nValores = len(valor_res).__str__()
    DNS_query.header.nAutoridades = len(valor_aut).__str__()
    DNS_query.header.nExtraVal = len(valor_ext).__str__()
    if 'R' in flags:
        flags = 'R'
    else:
        flags = ''
    if len(valor_aut) > 0:
        if 'R' in flags:
            flags += '+A'
        else:
            flags = 'A'
    DNS_query.header.flags = flags
    return DNS_query
