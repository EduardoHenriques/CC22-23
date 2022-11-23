# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from datetime import datetime
from os.path import exists
from infoBD import BD


class infoServer:
	def __init__(self, dirConfig):
		# --
		self.DD = []
		self.SS = []
		self. SP = []
		self.ST = []
		# --
		self.configDir = dirConfig
		self.logDir = ''
		self.all_logDir = ''
		self.DBDir = ''
		self.ST_DBDir = ''

		# ler linhas do config
		lines = []
		if exists(dirConfig):
			file = open(dirConfig, 'r')
			for line in file.readlines():
				if '#' not in line:
					lines.append(line)
			file.close()

		# analisar informaca das linhas do ficheiro e preencher os campos da classe
		for line in lines:
			if ' SP ' in line:
				self.SP.append((line.split(' SP ', 1)[1])[:-1])
			elif ' SS ' in line:
				self.SS.append((line.split(' SS ', 1)[1])[:-1])
			elif ' DD ' in line:
				self.DD.append((line.split(' DD ', 1)[1])[:-1])
			elif 'root ST ' in line:
				self.ST_DBDir = (line.split('root ST ', 1)[1])[:-1]
				if exists(self.ST_DBDir):
					servsTopo = open(self.ST_DBDir, 'r')
					for linha in servsTopo.readlines():
						if '#' not in line:
							self.ST.append(linha[:-1])
					servsTopo.close()
			elif ' DB ' in line:
				self.DBDir = (line.split('DB ', 1)[1])[:-1]
			elif ' LG ' in line and 'all LG ' not in line:
				self.logDir = (line.split('LG ', 1)[1])[:-1]
			elif 'all LG ' in line:
				self.all_logDir = (line.split('all LG ', 1)[1])[:-1]

		# quando o ficheiro de configuracao é lido, esta é a hora em que o servidor arrancou
		self.startTime = datetime.now()


if __name__ == '__main__':
	ex1 = infoServer('SPconfig.txt')
	BD_ex1 = BD(ex1.DBDir)
	print(BD_ex1)

	#print(ex1.DBDir)
	#print(ex1.ST_DBDir)
	#print(ex1.ST)
	#print(ex1.logDir)
	#print(ex1.logDir)
	#print(ex1.all_logDir)
	#print(ex1.startTime)

