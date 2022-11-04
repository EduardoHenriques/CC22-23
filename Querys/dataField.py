# DATA Fields de uma query

class data:
	
	def __init__(self, nome, tipo):
		self.queryInfo = (nome, tipo)
		self.respVals = "(null)"
		self.auhtorityVals = "(null)"
		self.extraVals = "(null)"
	
	def __str__(self):
		nome = self.queryInfo[0]
		tipo = self.queryInfo[1]
		out = '|DADOS|\nDados-Info.Nome:{}\nDados-Info.Tipo:{}\n---\nDados-RespVals:{}\nDados-autorithyVals:{}' \
			'\nDados-ExtraVals:{}\n'.format(nome, tipo, self.respVals.__str__(), self.auhtorityVals.__str__()
														, self.extraVals.__str__())
		
		return out
	