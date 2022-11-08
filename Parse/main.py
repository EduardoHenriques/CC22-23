# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from datetime import datetime
from os.path import exists


def lerConfigs(dir):
	fileExample = open(dir, 'r')
	now = datetime.now()
	count = 0
	i = 0
	stringsLidas, filter = [], []
	while True:
		count += 1
		line = fileExample.readline()
		if not line:
			break
		stringsLidas.append(line.strip())
		s = stringsLidas[i].strip()
		if not (s[:1] == "#" or s[:1] == ""):
			filter.append(s)
		i += 1
	
	fileExample.close()
	
	# informaçao foi filtrada, agora vamos abrir o(s) ficheiro(s) LOG e escrever tudo lá referente a este servidor.
	
	logs, all_Logs, dataBase, dataBaseST = '', '', '', ''
	name = filter[0].split(' ', 1)[0]  # example.com no exemplo do enunciado
	for val in filter:
		if 'all LG' in val:
			all_Logs += val.replace('all LG ', '', 1)  # transforma a linha coma  diretoria na diretoria de LOG_ALL.txt
		elif 'LG' in val:
			logs += val.split('LG ', 1)[1]  # transforma a linha coma  diretoria na diretoria de LOG_SERVER.txt
		elif 'DB' in val:
			dataBase = val.split('DB ', 1)[1]
		elif 'root' in val:
			dataBaseST = val.split('ST ', 1)[1]
	print(logs)
	print(all_Logs)
	print(dataBase)
	print(dataBaseST)
	if not exists(logs):
		logsFile = open(logs, 'a')
		logsFile.write('#Logs do servidor primario {}:\n'.format(name))
		[logsFile.write('[{}]:'.format(now.strftime('%Y/%m/%d|%H:%M:%S')) + str + '\n') for str in filter]
		logsFile.close()
	else:
		logsFile = open(logs, 'a')
		[logsFile.write('[{}]:'.format(now.strftime('%Y/%m/%d|%H:%M:%S')) + str + '\n') for str in filter]
		logsFile.close()
		
	if not exists(all_Logs):
		logsFile = open(all_Logs, 'a')
		logsFile.write('#Logs de todos os servidores\n')
		[logsFile.write('[{}]:'.format(now.strftime('%Y/%m/%d|%H:%M:%S')) + str + '\n') for str in filter]
		logsFile.close()
	else:
		logsFile = open(all_Logs, 'a')
		[logsFile.write('[{}]:'.format(now.strftime('%Y/%m/%d|%H:%M:%S')) + str + '\n') for str in filter]
		logsFile.close()
	return


if __name__ == '__main__':
	lerConfigs('SPconfig.txt')
