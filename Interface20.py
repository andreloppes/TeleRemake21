# pacotes de manipulação da interface gráfica
import PyQt5
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
#import pkg_resources.py2_warn

# demais pacotes necessários
import sys

# classes importadas
from interface_generated import Ui_MainWindow
from Data import Data
from Alarms import Alarms
from Log import Log
from SaveFile import SaveFile
from SerialPort import SerialPort
from Setup import Setup
from Update import Update
from WebApp import Web_App_Server
from Program import Program


#------------------------------------------------------------------------------------------------#
#Abertura da Interface Gráfica

# settings armazena os campos de configuracao na interface
settings = QtCore.QSettings('testa', 'interface_renovada')

# Roda janela
app = QtWidgets.QApplication(sys.argv)
app.setStyle("fusion")
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

#------------------------------------------------------------------------------------------------#
#DATA
#Instancia da classe Data
data= Data(ui)

#Adiciona os nomes das pistas a lista de tracks do hodometro
ui.trackOdometerComboBox.addItems(data.pistas)

#Chama método que apresenta os metros/volta d|e uma pi|sta selecionada pelo usuário
ui.trackOdometerComboBox.activated.connect(data.displayTracks)
data.displayTracks()

#Chama método que salva uma nova pista
ui.saveOdometerPushButton.clicked.connect(data.saveTrack)

#------------------------------------------------------------------------------------------------#
#ALARMS

#Instancia da classe Alarms
alarms= Alarms(data, ui, settings)

#Adiciona os nomes dos dados a lista de alarmes
ui.alarmComboBox.addItems(alarms.alarms)

#Adiciona os nomes dos tipos a lista de tipos de alarms
ui.alarmTypeComboBox.addItems(alarms.alarmTypes)

#Chama método que Restaura alarmes padrões
ui.restoreDefaultAlarmPushButton.clicked.connect(alarms.setDefaultAlarms)
alarms.setDefaultAlarms()

#Chama método que Salva um novo alarme
ui.saveAlarmPushButton.clicked.connect(alarms.saveAlarm)

#Chama método que apresenta configurações de alarme para determinado dado selecionado pelo usuário
ui.alarmComboBox.activated.connect(alarms.displayAlarm)

#------------------------------------------------------------------------------------------------#
#LOG

#Instancia para erros gerais
errorLog = Log(ui.errorLog, ui, maxElements=70)

#Instancia para erros no buffer de dados
bufferLog = Log(ui.textBrowser_Buffer, ui, maxElements=15)

#Botão que indica se a opção para exibir erros ou buffer esta ativada
ui.radioButton_errorLog.toggled.connect(lambda: errorLog.logEnabled("error"))
ui.radioButton_bufferLog.toggled.connect(lambda: bufferLog.logEnabled("buffer"))


#------------------------------------------------------------------------------------------------#
#SAVEFILE

#Instancia da classe SaveFile
saveFile= SaveFile(data, ui)

#Chama método que Inicia o "salvamento" dos dados em arquivo
ui.pushButton_SaveFile.clicked.connect(saveFile.startSave)

#Chama método que Interrompe o "salvamento" dos dados e salva/fecha o arquivo criado
ui.pushButton_StopSaveFile.clicked.connect(saveFile.stopSave)

#------------------------------------------------------------------------------------------------#
#SERIALPORT

#Instancia da classe SerialPort
serialPort= SerialPort(ui, errorLog)

#Exibi portas seriais disponiveis
serialPort.updatePorts()

#Botão que chama a atualização de portas seriais disponíveis
ui.pushButton_UpdatePorts.clicked.connect(serialPort.updatePorts)  

#Exibi os baudrates disponiveis
ui.comboBox_Baudrate.addItems(["115200", "38400", "1200", "2400", "9600", "19200", "57600" ])  

#Marca baudrate selecionado
#selection_baudrate= ui.comboBox_Baudrate.currentIndexChanged.connect()

#------------------------------------------------------------------------------------------------#
#SETUP

#Instancia de Setup
setup= Setup(ui, errorLog, alarms, settings)

#Botão que salva dados inseridos 
ui.pushButton_SaveSetupValues.clicked.connect(setup.saveSetup)

#Carregar dados de Setup salvos
setup.loadSetup()

#------------------------------------------------------------------------------------------------#
#CLASSE UPDATE

#Tempo de atulaização da interface
updateTime = ui.doubleSpinBox_UpdateTime.value() * 1000

#Instancia da classe Update
update= Update(updateTime, errorLog, bufferLog, ui, data, alarms, saveFile)

#Chama o método que atualiza as constants da interface quando alteradas
update.updateConstants()
ui.lineEdit_WheelPosMin.editingFinished.connect(update.updateConstants)
ui.lineEdit_WheelPosMax.editingFinished.connect(update.updateConstants)
ui.updateCounterP1.valueChanged.connect(update.updateConstants)
ui.updateCounterP2.valueChanged.connect(update.updateConstants)
ui.updateCounterP3.valueChanged.connect(update.updateConstants)
ui.updateCounterP4.valueChanged.connect(update.updateConstants)

#GRAFICOS "ENGINE / RELAY / BATTERY"
#cores dos gráficos
ui.checkBox_OilPressure.setStyleSheet('color:black')
ui.checkBox_FuelPressure.setStyleSheet('color:green')
ui.checkBox_EngineTemperature.setStyleSheet('color:red')
ui.checkBox_Voltage.setStyleSheet('color:blue')

#DIAGRAMAS GG
#range
ui.graphicsView_DiagramaGG_DD_2.setXRange(-2, 2)
ui.graphicsView_DiagramaGG_DD_2.setYRange(-2, 2)
ui.graphicsView_DiagramaGG_DE_2.setXRange(-2, 2)
ui.graphicsView_DiagramaGG_DE_2.setYRange(-2, 2)
ui.graphicsView_DiagramaGG_TD.setXRange(-2, 2)
ui.graphicsView_DiagramaGG_TD.setYRange(-2, 2)
ui.graphicsView_DiagramaGG_TE.setXRange(-2, 2)
ui.graphicsView_DiagramaGG_TE.setYRange(-2, 2)

#Verificar se atualização da interface esta acionada
ui.radioButton_updateInterface.toggled.connect(update.updateInterfaceEnabled)


#------------------------------------------------------------------------------------------------#
#WEBAPP

#Instancia da classe Web_App_Server
Web_App = Web_App = Web_App_Server("Servidor Web")

#Envia dados de processado em Data para o WebApps
Web_App.setData(data)

#Botões para habilitar ou desabilitar o WebApp
ui.pushButton_webAppStart.clicked.connect(lambda: Web_App.enable(ui))
ui.pushButton_webAppPause.clicked.connect(lambda: Web_App.disable(ui))

#------------------------------------------------------------------------------------------------#
#PROGRAM

#Instancia da classe Program
program= Program(data, saveFile, serialPort, Web_App, update, errorLog, ui)

#Botão que inicia o programa
ui.pushButton_StartProgram.clicked.connect(program.startProgram)

#Botão que pausa o programa
ui.pushButton_PauseProgram.clicked.connect(program.stopProgram)

#Método que para o Web_App e fecha a interface
def exit():
    if(Web_App.isRunning):
        Web_App.stop()
    sys.exit(app.exec_())

#Botão que fecha a janela 
ui.pushButton_Exit.clicked.connect(exit)  # botão para fechar a interface

#Botão que fecha a interface
ui.actionExit.triggered.connect(exit)
#------------------------------------------------------------------------------------------------#

#encerra programa
sys.exit(app.exec_())
