from mensagem import DNS


def querycliente(query):
    queryCL = "1123 meow.com MX R"
    parsed = query.split(" ")
    recursivo = True
    if len(parsed) < 5:
        recursivo = False
    queryDados = DNS(parsed[2], parsed[3], recursivo)
    return queryDados


def queryIP(query):
    parsed = query.split(" ")
    print(parsed[0])
    print(parsed[1])
    adress = (parsed[0], int(parsed[1]))
    return adress
