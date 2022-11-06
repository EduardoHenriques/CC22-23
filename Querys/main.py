from mensagem import DNS
import bin


def exemploQuery(nome, tipo, recursivo):
	msg1 = DNS(nome, tipo, recursivo)
	msg2 = msg1
	print(msg1)
	print(DNS.debug(msg1))


if __name__ == '__main__':
	exemploQuery('nomeExemplo', 'tipoExemplo', False)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
