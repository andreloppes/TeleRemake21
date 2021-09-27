#Pacotes importados
import PyQt5
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox

import serial
from serial import Serial, SerialException

#classes importadas
from Alarms import Alarms
from Data import Data
from Log import Log
from SaveFile import SaveFile
from SerialPort import SerialPort
from Update import Update
from WebApp import Web_App_Server
from Biblioteca import displayErrorMessage


# Classe responsável pela execução e interrupção do programa
# Faz a chamada para salvamentos, plotamento de gráficos, etc
class Program():
    #Construtor
    def __init__(self, data, saveFile, serialPort, Web_App, update, errorLog, ui):
        self.data = data  #Instancia da classe Data
        self.saveFile = saveFile  #Instancia da classe SaveFile
        self.serialPort = serialPort #Instancia da classe SerialPort
        self.ui= ui
        self.Web_App= Web_App
        self.errorLog= errorLog

        self.update = update # Instancia da classe da classe Update
        self.updateCounterMax = update.updateCounterMax  # numero de pacotes recebidos até atualizar a interface
        self.updateCounter = update.updateCounter
        self.updateInterfaceEnabled = True

        #Identificador e tamanho dos pacotes
        self.packIndexes = [1, 2, 3, 4]
        self.packSizes = self.data.pSizes
        self.stop = 0


    #MÉTODOS

    # Função que inicia a execução do programa
    def startProgram(self):
        try:
            # abre e configura a porta serial utilizando os valores definidos pelo usuário através da interface
            baudrate = int(self.ui.comboBox_Baudrate.currentText())
            port = str(self.ui.comboBox_SerialPorts.currentText())
            timeout = None
            print("alou")
            self.serialPort.openSerialPort(baudrate, port, timeout)
            

            # Inicializa programa e coloca constantes
            #self.update.updateConstants()
            print("oi")
            self.stop = 0
            self.updateTime = self.update.updateTime
            if self.ui.lineEdit_SampleRate1.text() == "" or self.ui.lineEdit_SampleRate2.text() == "" or self.ui.lineEdit_SampleRate3.text() == "" or self.ui.lineEdit_SampleRate4.text() == "":
                displayErrorMessage("Inserir taxa de amostragem dos pacotes")
            else:
                self.program()
                
    # O erro de porta serial é analisado pela exceção serial.SerialException. Esse erro é tratado pausando o programa e
    # utilizando uma caixa de diálogo, a qual informa ao usuário o erro encontrado
        except serial.serialutil.SerialException:
            self.errorLog.writeLog("startProgram: SerialException")
            self.stopProgram()
            dlg = QMessageBox(None)
            dlg.setWindowTitle("Error!")
            dlg.setIcon(QMessageBox.Warning)
            dlg.setText(
            "<center>Failed to receive data!<center> \n\n <center>Check Serial Ports and Telemetry System.<center>")
            dlg.exec_()


    # Roda em loop até o interrompimento do programa (stop =1)
    def program(self):
        print("program")
        if (self.stop == 0):
            # Le dados da porta serial
            self.buffer = self.serialPort.readFromSerialPort(self.packSizes, self.packIndexes)
            print("pg2")
            if len(self.buffer) != 0:
                # chamada da função updateDataAndInterface para analisar os dados recebidos e atualizar os mostradores da interface
                self.update.updateData(self.buffer, int(self.buffer[0]))
                if self.update.updateInterfaceEnabled:
                    self.update.updateInterface(self.buffer, int(self.buffer[0]))
                if self.saveFile.save == 1:
                        string = self.saveFile.createPackString(int(self.buffer[0]))
                        self.saveFile.writeRow(string)

            
            # Apos updateTime segundos, chama funcao program() novamente
            QtCore.QTimer.singleShot(self.update.updateTime, lambda: self.program())


    # Interrompe funcionamento do programa
    def stopProgram(self):
        self.stop = 1  # atualiza o valor da variavel stop, a qual é usada para verificar o funcionamento da interface

        # Fecha arquivo file e desconecta com a porta serial
        self.saveFile.stopSave()
        if self.serialPort.port.isOpen():
            self.serialPort.port.flushInput()
            self.serialPort.port.close()
        else:
            pass