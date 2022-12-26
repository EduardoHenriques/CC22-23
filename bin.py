# funcoes de encriptacao de formato normal strng para formato binario
# com algoritmo customizado e vice versa

import math

MIDDLE = 127  # para usar no algoritmo
SIZE = 9  # cada character vai ser encriptado numa string c/ 9 digitos binarios


def encriptar(str):
	if isinstance(str, int):
		str = str.__str__()
		
	strBin = ''
	for i in range(len(str)):
		ch = str[i]
		num = MIDDLE
		par = False
		ascii = ord(ch)  # passar um char p/ codigo ASCII
		# print(ascii)
		if ascii % 2 == 0:
			par = True
			num = MIDDLE - (ascii / 2)  # EXEMPLO: @ -> 64(ASCII) -> 127 - 32 = 95
		else:  # A -> 65(ASCII) -> 127 + 33 = 160
			num = MIDDLE + math.ceil(ascii / 2)  # B -> 66(ASCII) -> 127 - 33 = 94 (ect.)
		# print(num)
		res = format(int(num), "b").zfill(8)
		if par:
			res = '0' + res
		else:
			res = '1' + res
		strBin += res
		# print(res + ' -> ' + ch)
	
	return strBin


# converte uma string de zeros ou uns no seu inteiro correspondente(FUNÇAO AUXILIAR PARA DESCODIFICAR)
def binToInt(binWord):
	res = 0
	for i in range(len(binWord)):
		if binWord[i] == '1':
			res += math.pow(2, len(binWord) - i - 1)
	return res


def descriptar(strBin):
	str = ''
	# Primeiro transformar a string de numeros numa lista com strings de 9 digitos binarios
	# Depois descriptar cada elemento da string e concatena los
	listChar = [strBin[i:i + SIZE] for i in range(0, len(strBin), SIZE)]
	for i in range(len(listChar)):
		charBin = listChar[i]
		fst = charBin[0]  # primeiro character p/ ver se é par ou ímpar
		charBin = charBin[1:]
		num = binToInt(charBin)
		num = abs(num - MIDDLE) * 2
		if fst == '1':
			num -= 1
		str += chr(int(num))
	return str
