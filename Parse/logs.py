from os.path import exists
from datetime import datetime
from infoServer import infoServer
import sys
sys.path.append('C:\\Users\\Eduardo\\Desktop\\Querys')
from mensagem import DNS


def timestamp(ts):
    return '[{}]: '.format(ts.strftime('%Y:%m:%d|%H:%M:%S'))


def checkAllLogsFile(info):
    BOTH = True
    try:
        fLogsAll = open(info.all_logDir, 'a')  # caso a diretoria do ficheiro para todos os logs seja invalida ou
        fLogsAll.close()
    except FileNotFoundError:  # nao exista(''), a variavel BOTH é False
        BOTH = False
    return BOTH


def bootLog(info, IP_porta, timeout):
    prevAllLogs = True
    print(info.all_logDir)
    if not exists(info.all_logDir):
        prevAllLogs = False

    # se nao for fornecida uma diretoria allLogs, apenas sao feitas escritas no ficheiro do server

    BOTH = checkAllLogsFile(info)
    if BOTH:
        fLogsAll = open(info.all_logDir, 'a')
    # se a diretoria dada já existia, não será preciso criar o ficheiro allLogs e escrever 'all-log-file-created'
    # nos logs do servidor

    fLogs = open(info.logDir, 'a')
    print(prevAllLogs)

    # comeca o servidor
    fLogs.write(timestamp(info.startTime) + 'ST ' + IP_porta.__str__() + ' ' + timeout.__str__() + ' shy\n')
    if BOTH:
        fLogsAll.write(timestamp(info.startTime) + 'ST ' + IP_porta.__str__() + ' ' + timeout.__str__() + ' shy\n')

    # ficheiro de configs lido (escrito nos logs ou nos logs+logs globais)
    fLogs.write(timestamp(info.startTime) + 'EV config-file-read ' + info.configDir + '\n')
    if BOTH:
        fLogsAll.write(timestamp(info.startTime) + 'EV config-file-read ' + info.configDir + '\n')

    # se nao havia ficheiro p/ logs globais criado(e foi dada diretoria valida), é registada a sua criacao
    if not prevAllLogs:
        fLogs.write(timestamp(info.startTime) + 'EV log-file-created ' + info.all_logDir + '\n')

    # se houver base de dados(diretoria), foi lida
    if info.DBDir != '':
        fLogs.write(timestamp(info.startTime) + 'EV database-file-read ' + info.DBDir + '\n')
        if BOTH:
            fLogsAll.write(timestamp(info.startTime) + 'EV database-file-read ' + info.DBDir + '\n')

    fLogs.close()
    if BOTH:
        fLogsAll.close()


def writeLogLine(info, tipo_entrada, IP_Porta, str):
    fLogs = open(info.logDir, 'a')
    logLine = timestamp(datetime.now()) + tipo_entrada + ' ' + IP_Porta + ' ' + str + '\n'
    fLogs.write(logLine)
    fLogs.close()

    BOTH = checkAllLogsFile(info)
    if BOTH:
        fLogsAll = open(info.all_logDir, 'a')
        fLogsAll.write(logLine)
        fLogsAll.close()


def endSessionLog(info, IP_Porta):
    logEntry = timestamp(datetime.now()) + 'SP ' + IP_Porta + ' session-end\n'

    flogs = open(info.logDir, 'a')
    flogs.write(logEntry)
    flogs.close()

    if info.all_logDir != '':
        flogsAll = open(info.all_logDir, 'a')
        flogsAll.write(logEntry)
        flogsAll.close()


def main():
    ex1 = infoServer('SPconfig.txt')
    bootLog(ex1, '50', 2000)
    print('write server')
    q1 = DNS('nomeEx', 'tipoEx', False)
    writeLogLine(ex1, 'QR', '50', q1.debug())
    writeLogLine(ex1, 'QE', '50', q1.debug())
    print('fechar server')
    endSessionLog(ex1, '50')


if __name__ == '__main__':
    main()
