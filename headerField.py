import random


# Criar um header novo(para o cliente enviar uma mensagem DNS ao servidor).
# Para realizar o pedido, o servidor abre o  objeto da classe mensagem,
# muda a flag de Q, realiza o pedido e
# coloca nos campos mensagem.dataField.(resp/auth/extra)Vals.
# Antes de voltar a enviar a mensagem ao cliente, altera os campos do header
# de acordo com o respCode, o tamanho das listas de strings que colocou no mensagem.dataField.
# e se é servidor primario ou nao(flag A)


class header:
	def __init__(self, recursivo=False, resposta=False, autoritativo=False, id=-1):
		if id == -1:
			self.id = (random.randint(0, 65535)).__str__()
		else:
			self.id = id
			
		self.flags = 'Q'
		if recursivo:
			self.flags += '+R'
		self.respCode = '0'
		self.nValores = '0'
		self.nAutoridades = '0'
		self.nExtraVal = '0'

	def __str__(self):
		out = '|HEADER|\nHeader-ID: ' + self.id.__str__() + '\nHeader-Flags: ' \
			+ self.flags + '\nHeader-ResponseCode: ' + self.respCode.__str__() + '\nHeader-nValores: ' \
			+ self.nValores.__str__() + '\nHeader.nAutoridades: ' + self.nAutoridades.__str__() \
			+ '\nHeader-nExtraVals: ' + self.nExtraVal.__str__() + ''

		return out

	def __bin__(self):
		self.id = bin.encriptar(self.id)
		self.flags = bin.encriptar(self.flags)
		self.respCode = bin.encriptar(self.respCode)
		self.nValores = bin.encriptar(self.nValores)
		self.nAutoridades = bin.encriptar(self.nAutoridades)
		self.nExtraVal = bin.encriptar(self.nExtraVal)

	# metodo bytes funciona para uma string no modo debug


