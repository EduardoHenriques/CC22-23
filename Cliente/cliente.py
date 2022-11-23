import sys
sys.path.append('/home/me/CC22-23/Querys')
from mensagem import DNS


def querycliente():
    queryCL = "1123 example.com. MX R"
    parsed = queryCL.split(" ")
    recursivo = True
    if len(parsed) < 4:
        recursivo = False
    queryDados = DNS(parsed[1], parsed[2], recursivo)
    return queryDados


def queryIP():
    queryCL = "1123 example.com. MX R"
    parsed = queryCL.split(" ")

    return parsed[0]
