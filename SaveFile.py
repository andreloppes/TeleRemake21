from datetime import datetime

from Biblioteca import vectorToString
from Data import Data


#Classe responsável pelas operações de “salvamento” de dados e criação/gravação/fechamento de arquivos.
class SaveFile:
    #Construtor
    def __init__(self, data, ui):
        self.data= data   # Instancia da classe Data
        self.ui= ui       # Instancia gráfica
        self.save=0       # Atributo que indica status do salvamento 'Saving' ou 'Saving stop'

    #METODOS
    '''
    # Abre dialogo para escolher arquivo
    def selectFile():
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(MainWindow, "Escolha arquivo .txt",
                                                            "", "All Files (*);;Text Files (*.txt)")

        if len(fileName) > 5:
            ui.lineEdit_FileName.setText(fileName)
            return fileName
        else:
            return
    '''

    #Escreve o cabeçalho do arquivo, com informações inseridas pelo usuário no campo 'File Settings' da interface
    def headerFile(self):
        self.writeRow("***\n")
        self.writeRow("CARRO: " + str(self.ui.lineEdit_SetupCar.text()) + "\n")
        self.writeRow("PISTA: " + str(self.ui.lineEdit_SetupTrack.text()) + "\n")
        self.writeRow("PILOTO: " + str(self.ui.lineEdit_SetupDriver.text()) + "\n")
        self.writeRow("TEMPERATURA AMBIENTE: " + str(self.ui.lineEdit_SetupTemperature.text()) + "\n")
        self.writeRow("ANTIROLL: " +str(self.ui.lineEdit_SetupAntiroll.text()) + "\n")
        self.writeRow("PRESSAO PNEUS DIANTEIROS: " +str(self.ui.lineEdit_SetupTirePressureFront.text()) + "\n")
        self.writeRow("PRESSAO PNEUS TRASEIROS: " +str(self.ui.lineEdit_SetupTirePressureRear.text()) + "\n")
        self.writeRow("ANGULO DE ATAQUE DA ASA: " +str(self.ui.lineEdit_SetupWingAttackAngle.text()) + "\n")
        self.writeRow("MAPA MOTOR: " +str(self.ui.lineEdit_SetupEngineMap.text()) + "\n")
        self.writeRow("BALANCE BAR: " +str(self.ui.lineEdit_SetupBalanceBar.text()) + "\n")
        self.writeRow("DIFERENCIAL: " +str(self.ui.lineEdit_SetupDifferential.text()) + "\n")
        self.writeRow("TAXA DE AQUISICAO: "  + "\n")
        self.writeRow("COMENTARIOS: " +str(self.ui.textEdit_SetupComments.toPlainText()) + "\n")
        self.writeRow("POSICAO MAXIMA DO VOLANTE: " +str(self.ui.lineEdit_WheelPosMax.text()) + "\n")
        self.writeRow("POSICAO MINIMA DO VOLANTE: " +str(self.ui.lineEdit_WheelPosMin.text()) + "\n")
        self.writeRow("SUSPENSAO: " +str(self.ui.lineEdit_CalibrationConstant.text()) + "\n")
        self.writeRow("PACOTE1 " + self.ui.lineEdit_SampleRate1.text() + ' ' + vectorToString((list(self.data.dic.keys())[0:20]), ' '))
        self.writeRow("PACOTE2 " + self.ui.lineEdit_SampleRate2.text() + ' ' + vectorToString((list(self.data.dic.keys())[20:34]), ' '))
        self.writeRow("PACOTE3 " + self.ui.lineEdit_SampleRate3.text() + ' ' + vectorToString((list(self.data.dic.keys())[35:52]), ' '))
        self.writeRow("PACOTE4 " + self.ui.lineEdit_SampleRate4.text() + ' ' + vectorToString((list(self.data.dic.keys())[53:65]), ' '))
        self.writeRow("***\n\n")


    # Cria string unificada com dados do pacote packID, todos separados por espaço
    # Padroniza formato da string com dados obtidos para gravação em arquivo
    def createPackString(self, Id):        
        #Fatia lista de valores com intervalo de dados referente ao pacote do identificador ID 
        #e insere ID do pacote na primeira posição da lista
        if Id == 1:
            list=(self.data.packNames[0:19])
        elif Id == 2:
            list=(self.data.packNames[20:34])
        elif Id == 3:
            list=(self.data.packNames[35:52])
        elif Id == 4:
            list=(self.data.packNames[53:65])

        #cria string com dados separados por espaço
        delimiter = ' '
        vec = [Id]
        for key in list:                                                                                  
            vec.append(self.data.dicRaw[key])
        string = delimiter.join(str(x) for x in vec)
        string = string + '\n'
        return string


    # Criação e abertura do arquivo
    def startSave(self, arquivo):
        now = datetime.now()
        #Nome do arquivo selecionado pelo usuário
        arquivo = self.ui.lineEdit_FileName.text()

        # Define o nome do arquivo concatenando o nome definido pelo usuário e hora e minuto do início da gravação
        arquivo = arquivo + "_" + str(now.hour) + "_" + str(now.minute) + ".txt"
        
        print(arquivo)
        self.arq = open(arquivo, 'w')
        self.headerFile() # escreve as informações de cabelho no inicio do arquivo
        self.save = 1
        self.ui.label_12.setText("Saving...")  # informa ao usuário a situação atual de gravação de dados


    # Escreve dados de Setup no início do arquivo e dados recebidos de um pacote
    def writeRow(self, string):
        self.arq.write(string)


    # Interromper a gravação dos dados no arquivo txt
    def stopSave(self):
        if self.save != 0: #verifica se tem algum arquivo texto aberto sendo gravado
            hodometro= ('Total final de metros rodados: ')+ str(self.data.dic['hodometro'])
            self.writeRow(hodometro)
            self.save = 0  # atualiza o valor da variavel save
            self.arq.close()
            self.ui.label_12.setText("Saving stop...")  # informa ao usuário a situação atual de gravação de dados
