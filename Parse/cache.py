from datetime import datetime
from time import sleep

CACHE_LINHAS = 10
CACHE_COLUNAS = 8

PARA_NOME = 0
PARA_TIPO = 1
PARA_VALOR = 2
PARA_TTL = 3
PARA_PRI = 4
PARA_ORIGEM = 5
PARA_TIMESTAMP = 6
PARA_STATUS = 7


def datetime_to_seconds(string):
	return string.timestamp()


# check se uma linha da cache expirou
def expirou(linha):
	if linha[PARA_ORIGEM] != "OTHER":
		return False
	ttl_linha = float(linha[PARA_TTL])
	timestamp_linha = float(linha[PARA_TIMESTAMP])
	currTime = datetime_to_seconds(datetime.now())
	
	if float(currTime) - timestamp_linha > ttl_linha/1000:
		return True
	return False
	

def str_to_CacheEntry(str):
	linhaCache = [CACHE_COLUNAS]
	linhaCache = ["...", "...", "...", "...", "...", "...", "...", "...", "..."]
	linhaCache[PARA_TIMESTAMP] = datetime_to_seconds(datetime.now()).__str__()
	linhaCache[PARA_PRI] = "0"
	entradas = str.split(" ")
	for i in range(len(entradas)):
		match i:
			case 0:
				linhaCache[PARA_TIPO] = entradas[i].__str__()
			case 1:
				linhaCache[PARA_NOME] = entradas[i].__str__()
			case 2:
				linhaCache[PARA_VALOR] = entradas[i].__str__()
			case 3:
				linhaCache[PARA_TTL] = entradas[i].__str__()
			case 4:
				linhaCache[PARA_PRI] = entradas[i].__str__()
	
	return linhaCache


class cache:
	# encher a cache com valores vazios e com o timestamp correto
	def __init__(self, start_time):
		
		self.cache = [[]]
		self.n_entradas = 0
		self.startup = datetime_to_seconds(datetime.now())
		self.cache = [["..." for x in range(CACHE_COLUNAS)] for y in range(CACHE_LINHAS)]
		for i in range(CACHE_LINHAS):
			self.cache[i][PARA_STATUS] = "FREE"
			self.cache[i][PARA_TIMESTAMP] = datetime_to_seconds(datetime.now())
	
	def showCache(self):
		print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.cache]))
	
	# apenas para SERVIDORES SECUNDARIOS...
	def atualizarCache(self, domain):
		for i in range(CACHE_LINHAS):
			if (self.cache[i][PARA_STATUS] != "FREE") and (self.cache[i][PARA_VALOR] == domain.__str__()):
				self.cache[i][PARA_STATUS] = "FREE"
	
	# funcao que da match a uma linha com o tipo e o valor, e atualiza as entradas da cache
	def matchCache(self, tipo, valor):
		linhasMatched = []
		for i in range(CACHE_LINHAS):
			linha = self.cache[i]
			if expirou(linha):
				self.cache[i][PARA_STATUS] = "FREE" # ddf
				print(self.cache[i])
			elif linha[PARA_TIPO] == tipo and linha[PARA_VALOR] == valor:
				linhasMatched.append(linha)
		return linhasMatched
		
	# verifica se existe uma linha igual á que vamos procurar, return true se nao foi preciso inserir a linha
	def existe(self, linha):
		for i in range(CACHE_LINHAS):    # verifica se uma linha da cache como esta ja existe
			l = self.cache[i]
			if linha[PARA_NOME] == l[PARA_NOME] and linha[PARA_VALOR] == l[PARA_VALOR] and \
				linha[PARA_TIPO] == l[PARA_TIPO] and linha[PARA_TTL] == l[PARA_TTL] and linha[PARA_PRI] == l[PARA_PRI]:
				if l[PARA_ORIGEM] != "OTHER":
					return True     # pedido ignorado porque a linha tem origem FILE ou SP
				else:
					l[PARA_TIMESTAMP] = datetime_to_seconds(datetime.now())  # linha ja existe, timestamp levou refresh
					return True
		return False    # nao existe uma linha como esta na cache
		
		# recebe uma linha [nome,tipo,valor,ttl,prioridade, (origem), (timestamp), VALID]
	def inserirCache(self, linha):
		if linha[PARA_ORIGEM] != "OTHER":
			self.permaInsert(linha)
		elif not self.existe(linha): # nao existe uma linha como esta na cache e tem origem OTHER
			for i,l in reversed(list(enumerate(self.cache))):
				if l[PARA_STATUS] == "FREE":
					self.cache[i] = linha
					self.cache[i][PARA_STATUS] = "VALID"
	
	# insersao com prioridade, insere na primeira linha da cache que esta livre(FILE/SP)
	def permaInsert(self,linha):
		for i in range(CACHE_LINHAS):
			if self.cache[i][PARA_STATUS] == "FREE":
				self.cache[i] = linha
				self.cache[i][PARA_TIMESTAMP] = datetime_to_seconds(datetime.now())
				return
		return
	
	
		
		
if __name__ == '__main__':
	cache1 = cache(datetime.now())
	linha_teste = ["example.com", "A", "125.192.02.31", "2450", "0", "OTHER",
						datetime_to_seconds(datetime.now()), "1", "VALID"]
	
	cache1.cache[3] = linha_teste
	cache1.showCache()
	
	sleep(3)
	res = cache1.matchCache("A", "125.192.02.31")
	cache1.showCache()
	
	
	
