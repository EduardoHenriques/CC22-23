
from datetime import datetime
from functools import cmp_to_key
from os.path import exists
from time import sleep
from cache import cache
from cache import datetime_to_seconds


def replaceDefault(line, def1, def2):
    if "@" in line:
        line.replace("@", def1)
    elif "TTL" in line:
        line.replace("TTL", def2)
    return line


# funcao que recebe uma linha da base de dados e retorna uma lista com 8 elementos(linha da cache) para inserir na cache
def linhaBD_to_linhaCache(linhaBD, origem):
    linhaCache = linhaBD.split(" ")
    size = len(linhaCache)
    if size == 4:
        linhaCache.append("0") # se tem TTL e nao tem prioridade, atribuimos a mais baixa
    linhaCache.extend((origem, datetime_to_seconds(datetime.now()), "VALID"))
    return linhaCache


class BD:
    def __init__(self, dirBD):
        self.linhas = [] # uma lista com as linhas da base de dados
        self.defaultDom = "" # o dominio que vamos escrever na cache quando foi lida uma linha que tenha DEFAULT
        self.defaultTTL = "" # o TTL default para ser substituido na palavra TTL quando adicionarmos as linhas na cache
        self.cache = cache()
        # verificar se tem uma base de dados(SP)
        if exists(dirBD):
            file = open(dirBD, 'r')
            for line in file.readlines():
                if '#' not in line or line == '\n':
                    if "@ DEFAULT" in line:
                        self.defaultDom = line.split("@ DEFAULT ")[1][:-1]
                    elif "TTL DEFAULT" in line:
                        self.defaultTTL = line.split("TTL DEFAULT ")[1][:-1]
                    else:
                        line = line.replace("@", self.defaultDom)
                        line = line.replace("TTL", self.defaultTTL)
                        self.linhas.append(replaceDefault((line[:-1]), self.defaultDom, self.defaultTTL))
            file.close()

    def __str__(self):
        str = ''
        for line in self.linhas:
            str = str + line + '\n'
        str = str + "DEFAULT DOMAIN:" + self.defaultDom + "\nDEFAULT TTL:" + self.defaultTTL + "\n"
        return str

  
if __name__ == '__main__':
    dados1 = BD("dataBase_SP.db")
    print(dados1.__str__())
    for linha in dados1.linhas:
        linhaC = linhaBD_to_linhaCache(linha, "FILE")
        print(linhaC)
        dados1.cache.inserirCache(linhaC)
    dados1.cache.showCache()


