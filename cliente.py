from mensagem import DNS


def querycliente(query):
    parsed = query.split(" ")
    recursivo = True
    if len(parsed) < 5:
        recursivo = False
    queryDados = DNS(parsed[2], parsed[3], recursivo)
    return queryDados


def queryIP(query):
    parsed = query.split(" ")
    adress = (parsed[0], int(parsed[1]))
    return adress
