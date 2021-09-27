import serial
from serial import Serial, SerialException
import sys
import glob

'''
Classe responsavel pelas operações com portas seriais, como atualização e listamento das portas disponiveis, abertura, 
leitura e fechamento de uma porta serial selecionada. Ela que recebe e lê os dados enviado pelo rádio Xbee, enviado 
para as demais classes do código.
'''

class SerialPort:
    #Método Construtor
    def __init__(self, ui, errorLog):
        self.errorLog= errorLog       #Instancia da classe Log
        self.ui= ui                   #Instancia gráfica 
        self.port = serial.Serial()   #Atributo

    # Retorna uma Lista com os nomes das portas seriais disponiveis
    def listSerialPorts(self):
        #Leitura de portas seriais disponiveis de acordo com sistema operacional utilizado
        #sistema operacional Windows
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        
        #sistema operacional Linux ou Unix
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        
        #sistema operacional Mac OS
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')

        #sistema não suportado pela interface, lança exceção da classe padrão EnvironmentError
        else:
            raise EnvironmentError('Unsupported platform')
        
        # Deixa todos portas seriais disponiveis fechadas para o programa, deixando o usuário selecionar qual deseja abrir
        # Cria vetor com lista de portas disponiveis a serem retornadas
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            #lança exceção, caso não seja possivel fechar uma porta serial, indicando que ela está 
            #sendo utilizada por outro programa do SO, não a incluindo na lista de disponiveis ao usuário
            except (OSError, serial.SerialException):
                pass
        
        #retorna vetor (result) com lista de portas seriais disponiveis ao usuario
        return result


    # Atualiza a lista de portas seriais disponiveis
    def updatePorts(self):
        self.ui.comboBox_SerialPorts.clear() #apaga lista atual
        ports= self.listSerialPorts()
        self.ui.comboBox_SerialPorts.addItems(ports) #mostra lista atualizada de portas


    # Abre porta serial selecionada
    def openSerialPort(self, baudrate, selectedPort, timeout):
        #configura parâmetros, como taxa de transmissão (baudrate), para a abertura da porta serial
        self.port.baudrate = baudrate
        self.port.port = selectedPort
        self.port.timeout = timeout
        #abre porta selecionada
        self.port.open()
        print("abriu")


    # Le buffer da porta serial, verificadobufferSize é uma lista com os tamanhos dos pacotes e firstByteValues
    # é uma lista com os numeros dos pacotes (1,2,3,4)
    def readFromSerialPort(self, bufferSize, firstByteValues):
        #Leitura dos primeiro dois bytes do vetor, verificando se buffer recebido esta no formato correto
        while True:
            # espera receber algo na porta serial
            while (self.port.inWaiting() == 0):
                pass
            
            # Verifica se primeiro byte corresponde a um dos pacotes (1,2,3 ou 4)
            # Faz comparações implementadas, em que sempre o primeiro e segundo byte do pacote tem que ser o núm. do pacote e 5 respectivamente
            read_buffer = b''
            firstByte = self.port.read()
            if int.from_bytes(firstByte, byteorder='big') in firstByteValues:
                read_buffer += firstByte
                # le o segundo byte de inicio
                a = self.port.read()
                if int.from_bytes(a, byteorder='big') == 5:
                    read_buffer += a
                    break
                else:
                    self.errorLog.writeLog("Leitura: segundo byte com valor inesperado. Leu-se " + str(firstByte) + ", esperava-se 5")
                
            # se o byte lido nao for 1, 2 3 ou 4, quer dizer que algum dado se perdeu. Buffer em formato incorreto.
            # lança mensagem de erro na instancia errorLog
            else:
                self.errorLog.writeLog("Leitura: primeiro byte com valor inesperado. Leu-se " + str(firstByte) + ", esperava-se de 1 a 4")

        #Leitura do resto do buffer, verificando se este está completo para aquele respectivo pacote
        while True:
            #index é o numero do pacote que o buffer esta enviando
            index = int.from_bytes(firstByte, byteorder='big') - 1
            #le quando bytes tem no vetor, além dos dois já lidos anteriormente
            byte = self.port.read(size=int(bufferSize[index] - 2))
            read_buffer += byte

            # Compara se o pacote tem o tamanho esperado
            # Faz comparações implementadas, em que sempre o penultimo e o último valor do pacote tem que ser 9 e 10 respectivamente
            if(len(read_buffer) == bufferSize[index]):
                if int(read_buffer[bufferSize[index]-2]) == 9:
                    # Chegou no fim do pacote
                    if int(read_buffer[bufferSize[index]-1]) == 10:
                        break
                    else:
                        self.errorLog.writeLog("Leitura: ultimo dado diferente de byte 10" + str(read_buffer))
                        return []
                else:
                    self.errorLog.writeLog("Leitura: penultimo dado diferente de byte 9")
                    return []
        
        # Retorna buffer de dados lidos do respectivo pacote
        return read_buffer
