from mensagem import DNS
import bin


def exemploQuery(nome, tipo, recursivo):
	msg1 = DNS(nome, tipo, recursivo)
	print(msg1)
	print("\n....\n")
	msg1.__bin__()
	print(msg1)
	
	
if __name__ == '__main__':
	exemploQuery('nomeExemplo', 'tipoExemplo', False, )

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
