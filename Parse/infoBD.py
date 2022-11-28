from datetime import datetime
from os.path import exists
from time import sleep

CACHE_LINHAS = 50
CACHE_COLUNAS = 9

PARA_NOME = 0
PARA_TIPO = 1
PARA_VALOR = 2
PARA_TTL = 3
PARA_ORDER = 4
PARA_ORIGEM = 5
PARA_TIMESTAMP = 6
PARA_NUM_ENTRADA = 7
PARA_STATUS = 8


class BD:
	def __init__(self, dirBD, start_time):
		self.linhas = []
		self.defaultDom = ""
		self.defaultTTL = ""
		self.cache = [[]]
		
		if exists(dirBD):
			file = open(dirBD, 'r')
			print("entrou")
			for line in file.readlines():
				if '#' not in line or line == '\n':
					if "@ DEFAULT" in line:  # verifica se existem valores "default" que deverao ser substituidos na BD
						self.defaultDom = line.split("@ DEFAULT ")[1][:-1]
					elif "TTL DEFAULT" in line:
						self.defaultTTL = line.split("TTL DEFAULT ")[1][:-1]
					else:
						line = line.replace("@", self.defaultDom)
						line = line.replace("TTL", self.defaultTTL)
					self.linhas.append(replaceDefault((line[:-1]), self.defaultDom, self.defaultTTL))  # caso existam,
			file.close()  # sao substituidos
		self.cache = [["..." for x in range(CACHE_COLUNAS)] for y in range(CACHE_LINHAS)] # encher a cache com valores
		for i in range(CACHE_LINHAS): # "vazios" nas suas linhas, que serao substituidos á medida que as linhas
			self.cache[i][PARA_STATUS] = "FREE" # sao atualizadas
			self.cache[i][PARA_TIMESTAMP] = datetime_to_milliseconds(start_time)
	
	def __str__(self):
		str = ''
		for line in self.linhas:
			str = str + line + '\n'
		str = str + "DEFAULT DOMAIN:" + self.defaultDom + "\nDEFAULT TTL:" + self.defaultTTL + "\n"
		return str
	
	def showCache(self):
		for y in range(CACHE_LINHAS):
			line = ""
			for x in range(CACHE_COLUNAS):
				line += self.cache[y][x]
			print(line)
	
	def atualizarCache(self, linha):
		if not checkTTL(self.cache[linha][PARA_TIMESTAMP], "200"):
			self.cache[linha][PARA_VALOR] = "TS_INVALID"
		self.cache[linha][PARA_TIMESTAMP] = datetime_to_milliseconds(datetime.now())


# recebe o timestamp de uma linha de cache, ou seja, o tempo em que a linha foi colocada lá, em ms
# recebe o TTL aceitavel do servidor(em ms) e faz a diferenca entre o timestamp do presente e o timestamp em que a linha
# foi colocada. Caso seja um intervalo maior do que o aceitável, a linha é a
def checkTTL(ts_cache, TTL_server):
	ms_presente = datetime_to_milliseconds(datetime.now())
	ms_linha_cache = ts_cache
	ms_server = TTL_server
	print("-----INSERSAO EM LINHA--------")
	dif = int(ms_presente) - int(ms_linha_cache)
	if dif > int(ms_server):
		return False
	return True


def datetime_to_milliseconds(string):
	return ((string.timestamp() * 1000).__int__()).__str__()


def replaceDefault(line, def1, def2):
	if "@" in line:
		line.replace("@", def1)
	elif "TTL" in line:
		line.replace("TTL", def2)
	return line


if __name__ == '__main__':
	dados1 = BD("dataBase_SP.db", datetime.now())
	print(dados1.defaultTTL)
	out = dados1.__str__()
	print(out)



