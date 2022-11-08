import pickle
import sys
sys.path.append('C:\\Users\\me\\Desktop\\CC22-23\\Querys')
from mensagem import DNS


def querycliente():
    queryCL = "53 example.com. MX R"
    parsed = queryCL.split(" ")
    recursivo = True
    if len(parsed) < 4:
        recursivo = False
    queryDados = DNS(parsed[1], parsed[2], recursivo)
    bit1 = pickle.dumps(queryDados)
    return bit1


def queryIP():
    queryCL = "53 example.com. MX R"
    parsed = queryCL.split(" ")

    return parsed[0]
