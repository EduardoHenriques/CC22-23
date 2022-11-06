import bin


# DATA Fields de uma query


class data:
	
	def __init__(self, nome, tipo):
		self.queryInfo = (nome, tipo)
		self.respVals = ["(null)"]
		self.auhtorityVals = ["(null)"]
		self.extraVals = ["(null)"]
	
	def __str__(self):
		nome = self.queryInfo[0]
		tipo = self.queryInfo[1]
		out = '|DADOS|\nDados-Info.Nome: {}\nDados-Info.Tipo: {}\n'.format(self.queryInfo[0], self.queryInfo[1])
		for str in self.respVals:
			out += '\nDados-respVals: ' + str
		for str in self.auhtorityVals:
			out = out + '\nDados-authorityVals: ' + str
		for str in self.extraVals:
			out = out + '\nDados-extraVals: ' + str
		
		return out
	
	def __bin__(self):
		nome = self.queryInfo[0]
		tipo = self.queryInfo[1]
		self.queryInfo = (bin.encriptar(nome), bin.encriptar(tipo))
		self.respVals = [bin.encriptar(str) for str in self.respVals]
		self.auhtorityVals = [bin.encriptar(str) for str in self.auhtorityVals]
		self.extraVals = [bin.encriptar(str) for str in self.extraVals]

	def debug(self):
		out = self.queryInfo[0] + ',' + self.queryInfo[1] + ';'
		return out
		