
from datetime import datetime
from functools import cmp_to_key
from os.path import exists
from time import sleep
from cache import cache


def replaceDefault(line, def1, def2):
	if "@" in line:
		line.replace("@", def1)
	elif "TTL" in line:
		line.replace("TTL", def2)
	return line


class BD:
	def __init__(self, dirBD, start_time):
		self.linhas = []
		self.defaultDom = ""
		self.defaultTTL = ""
		self.cache = cache(datetime.now())
		# verificar se tem uma base de dados(SP)
		if exists(dirBD):
			file = open(dirBD, 'r')
			for line in file.readlines():
				if '#' not in line or line == '\n':
					if "@ DEFAULT" in line:
						self.defaultDom = line.split("@ DEFAULT ")[1][:-1]
					elif "TTL DEFAULT" in line:
						self.defaultTTL = line.split("TTL DEFAULT ")[1][:-1]
					else:
						line = line.replace("@", self.defaultDom)
						line = line.replace("TTL", self.defaultTTL)
					self.linhas.append(replaceDefault((line[:-1]), self.defaultDom, self.defaultTTL))
			file.close()

	def __str__(self):
		str = ''
		for line in self.linhas:
			str = str + line + '\n'
		str = str + "DEFAULT DOMAIN:" + self.defaultDom + "\nDEFAULT TTL:" + self.defaultTTL + "\n"
		return str
	
  
if __name__ == '__main__':
	dados1 = BD("dataBase_SP.db", datetime.now())
	print(dados1.__str__())
