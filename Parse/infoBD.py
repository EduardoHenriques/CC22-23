from datetime import datetime
from os.path import exists


class BD:
    def __init__(self, dirBD):
        self.linhas = []
        if exists(dirBD):
            file = open(dirBD, 'r')
            for line in file.readlines():
                if '#' not in line or line == '\n':
                    self.linhas.append(line[:-1])
            file.close()
        self.numLinhas = len(self.linhas)

    def __str__(self):
        out = ''
        for line in self.linhas:
            out = out + line + '\n'
        return out









