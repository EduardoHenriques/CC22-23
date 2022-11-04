import random


# Criar um header novo(para o cliente enviar uma mensagem DNS ao servidor)


class header:
	def __init__(self, recursivo=False):
		self.id = random.randint(0, 65535)
		self.flags = 'Q'
		if recursivo:
			self.flags = 'Q+R'
		self.respCode = 0
		self.nValores = 0
		self.nAutoridades = 0
		self.nExtraVal = 0
	
	def __str__(self):
		out = '|HEADER|\nHeader-ID: ' + self.id.__str__() + '\nHeader-Flags: ' \
			+ self.flags + '\nHeader-ResponseCode: ' + self.respCode.__str__() + '\nHeader-nValores: ' \
			+ self.nValores.__str__() + '\nHeader.nAutoridades: ' + self.nAutoridades.__str__() + '\nHeader-nExtraVals: ' \
			+ self.nExtraVal.__str__() + ''
		return out
