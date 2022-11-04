from headerField import header
from dataField import data


# classe co mensagens que vao ser enviadas entre clientes e servidores

class DNS:
	# Criar uma query nova (o cliente irá mandá-la para um servidor). Flags: Q + R ou só Q
	def __init__(self, nome, tipo, recursivo):
		self.header = header(recursivo)
		self.data = data(nome, tipo)
	
	def __str__(self):
		out = self.header.__str__() + "\n\n" + self.data.__str__()
		return out
