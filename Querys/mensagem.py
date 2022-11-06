import bin
from headerField import header
from dataField import data


# classe com mensagens DNS que vao ser enviadas entre clientes e servidores.
# AVISO: tudo o que tem a ver com encriptar e descriptar é temporário, só estou a experimentar
# nao apagues nada, eu apago isso eventualmente


class DNS:
	# Criar uma query nova (o cliente irá mandá-la para um servidor). Flags: Q + R ou só Q
	def __init__(self, nome, tipo, recursivo):
		self.header = header(recursivo)
		self.data = data(nome, tipo)
	
	# Transforma o objeto DNS numa string
	def __str__(self):
		out = self.header.__str__() + "\n\n" + self.data.__str__()
		return out
	
	# Codifica todos os campos do objeto DNS com o algoritmo em bin.py
	def __bin__(self):
		self.header.__bin__()
		self.data.__bin__()
		return
	

