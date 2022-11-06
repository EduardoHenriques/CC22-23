# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from datetime import datetime


def filtroFicheiro(dir, dirLOGs):
	fileExample = open(dir, 'r')
	fileLOG = open(dirLOGs, 'a')
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
		if not(s[:1] == "#" or s[:1] == ""):
			print(s)
			fileLOG.write('[{}]: Leu \'{}\' do ficheiro {}\n'.format(now.strftime('%Y/%m/%d|%H:%M:%S'), s, dir))
			filter.append(s)
		i += 1

	fileExample.close()
	fileLOG.close()
	return


if __name__ == '__main__':
	filtroFicheiro('example.txt', 'logs.txt')
