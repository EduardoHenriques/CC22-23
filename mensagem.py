import bin
import headerField
from headerField import header
from dataField import data


# classe com mensagens DNS que vao ser enviadas entre clientes e servidores.
# AVISO: tudo o que tem a ver com encriptar e descriptar é temporário, só estou a experimentar
# nao apagues nada, eu apago isso eventualmente


class DNS:
    # Criar uma query nova (o cliente irá mandá-la para um servidor). Flags: Q + R ou só Q
    def __init__(self, nome, tipo, recursivo):
        self.header = header(recursivo)
        self.data = data(nome, tipo)

    # Transforma o objeto DNS numa string
    def __str__(self):
        out = self.header.__str__() + "\n\n" + self.data.__str__()
        return out

    # Codifica todos os campos do objeto DNS com o algoritmo em bin.py
    def __bin__(self):
        self.header.__bin__()
        self.data.__bin__()
        return

    # colocar uma mensagem DNS no modo debug para facilitar o seu envio
    def debug(self):
        resposta = False
        if 'Q' not in self.header.flags:
            resposta = True
        out = ''
        out = out + self.header.id.__str__() + ',' + self.header.flags + ',' + self.header.respCode \
              + ',' + self.header.nValores + ',' + self.header.nAutoridades + ',' + self.header.nExtraVal \
              + ';' + self.data.queryInfo[0] + ',' + self.data.queryInfo[1]
        if resposta:
            out += '\n'
            out += debugAux(self.data.respVals)
            out += debugAux(self.data.auhtorityVals)
            out += debugAux(self.data.extraVals)
        else:
            out += ';\n'
        return out

    def debugLog(self):
        out = ''
        out = out + self.header.id.__str__() + ',' + self.header.flags + ',' + self.header.respCode \
              + ',' + self.header.nValores + ',' + self.header.nAutoridades + ',' + self.header.nExtraVal \
              + ';' + self.data.queryInfo[0] + ',' + self.data.queryInfo[1] + ';'
        return out


# percorre uma lista de strings e coloca-as em modo debug com ',' e ';' nos locais apropriados
def debugAux(listaDados):
    out = ''
    for i in range(len(listaDados)):
        out += listaDados[i]
        if i != len(listaDados) - 1:
            out += ',\n'
        else:
            out += ';\n'
    return out
