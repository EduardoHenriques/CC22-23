# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def filtroFicheiro(dir):
	config = open(dir, 'r')
	count = 0
	stringsLidas, filter = [], []
	while True:
		count += 1
		line = config.readline()
		if not line:
			break
		stringsLidas.append(line.strip())

	for i in range(len(stringsLidas)):
		s = stringsLidas[i].strip()
		if not(s[:1] == "#" or s[:1] == ""):
			print(s)
			filter.append(s)

	config.close()


if __name__ == '__main__':
	filtroFicheiro('config.txt')
