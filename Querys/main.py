# This is a sample Python script.

from mensagem import DNS
from headerField import header
from dataField import data


def exemploQuery(nome, tipo, recursivo):
    msg1 = DNS(nome, tipo, recursivo)
    print(msg1.__str__())


if __name__ == '__main__':
    exemploQuery('nomeExemplo', 'tipoExemplo', True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
