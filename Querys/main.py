from mensagem import DNS
import pickle


def exemploQuery(nome, tipo, recursivo):
	msg1 = DNS(nome, tipo, recursivo)
	msg2 = DNS(nome, tipo, recursivo)
	
	msg1.header.flags = ''
	msg1.header.nValores = '1'
	msg1.header.nAutoridades = '2'
	msg1.header.nExtraVal = '1'
	msg1.data.respVals = ["o"]
	msg1.data.auhtorityVals = ["zeca", "é"]
	msg1.data.extraVals = ["gay"]
	print(DNS.debug(msg2))
	print(DNS.debug(msg1))
	print(msg1)
	
	print(DNS.debug(msg1))
	bit1 = pickle.dumps(msg1)
	print(bit1)
	print('\nUnpickle\n')
	msg1clone = pickle.loads(bit1)
	print(DNS.debug(msg1clone))


if __name__ == '__main__':
	exemploQuery('nomeExemplo', 'tipoExemplo', False)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
