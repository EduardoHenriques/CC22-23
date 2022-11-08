import sys

sys.path.append('C:\\Users\\me\\Desktop\\CC22-23\\Querys')
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


def answer(DNS_query, file):
    nome = DNS_query.data.queryInfo[0]
    tipo = DNS_query.data.queryInfo[1]
    flags = DNS_query.header.flags
    valor_res = []
    valor_aut = []
    valor_ext = []
    linhas = file.readlines()
    nome = get_default(nome, linhas)
    print(nome)
    for linha in linhas:
        fstelem = linha.split(' ')[0]
        if nome == fstelem and tipo in linha:
            valor_res.append(linha[:-1])
        if nome == fstelem and 'NS' in linha:
            valor_aut.append(linha[:-1])
        if 'A' in linha:
            if verifica_extras(valor_res, valor_aut, linha):
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
    DNS_query.header.flags= flags
