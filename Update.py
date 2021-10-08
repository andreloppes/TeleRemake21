#pacotes importados
import numpy as np
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import glob
import time
#classes importadas
from Data import Data
from Alarms import Alarms
from Log import Log
from Biblioteca import vectorToString
from SaveFile import SaveFile
'''
teste
'''

class Update:
    def __init__(self, updateTime, errorLog, bufferLog, ui, data, alarms, saveFile):
        self.data = data #instancia da Calsse Data
        self.updateTime = updateTime
        self.dataFile = saveFile #Instancia classe SaveFile
        self.lastBuffers = bufferLog #Verifica condição de botão da interface
        self.log = errorLog #Verifica condição de botão da interface
        self.ui = ui        #Instancia grafica
        self.alarms = alarms

        self.updateCounterMax = [0, 0, 0, 0] # numero de pacotes recebidos até atualizar a interface
        self.updateCounter = [0, 0, 0, 0]         # numero de pacotes recebidos desde a ultima atualizacao da interface
        self.enabled = True        # variavel que habilita ou desabilita a atualizacao da interface

        #Vetores para plotagem de gráficos na aba "Engine | Battery | Relay" da interface
        self.arrayTemp = np.zeros(50)
        self.arrayFuelP = np.zeros(50)
        self.arrayOilP = np.zeros(50)
        self.arrayBattery = np.zeros(50)
        self.arrayTime2 = np.zeros(50)
        self.arrayTime3 = np.zeros(50)


    def rollArrays(self): 
        #funcao para manter o vetor ordenado da mensagem mais antiga a mais nova
        #atualizando o ultimo valor e "empurrando" em uma posicao
        self.arrayBattery = np.roll(self.arrayBattery, -1)
        self.arrayBattery[-1] = self.data.dic['batVoltage']
        self.arrayOilP = np.roll(self.arrayOilP, -1)
        self.arrayOilP[-1] = self.data.dic['oleoP']
        self.arrayTemp = np.roll(self.arrayTemp, -1)
        self.arrayTemp[-1] = self.data.dic['ect']
        self.arrayFuelP = np.roll(self.arrayFuelP, -1)
        self.arrayFuelP[-1] = self.data.dic['fuelP']
        self.arrayTime2 = np.roll(self.arrayTime2, -1)
        self.arrayTime2[-1] = self.data.dic['time2']
        self.arrayTime3 = np.roll(self.arrayTime3, -1)
        self.arrayTime3[-1] = self.data.dic['time3']


    def updateData(self, buffer, packID):
    # Atualiza dados em Data e Atualiza campos respectivos na interface
        if (self.data.updateDataFunctions[packID](buffer) == 0):
            self.log.writeLog(" updateData: Pacote " + str(packID) + "com tamanho diferente do configurado")

        # Chama função que atualiza graficos da aba 'Engine | Battery | Realy da interface' da interface
        if packID == 2 or packID == 3:
            self.rollArrays()


    #Método que verifica se atualização da interface está ativada pelo usuário
    def updateInterfaceEnabled(self):
        if self.ui.radioButton_updateInterface.isChecked():
            self.enabled = True
            print('Ativou Interface')
        else:
            self.enabled = False
            print('Desativou Interface')


    def updateInterface(self, buffer, packID):
    # Chama funcao updatePxInterface
        if self.updateCounter[packID-1] >= self.updateCounterMax[packID-1]:
            self.updatePXInterface(packID)
            self.updateCounter[packID-1] = 0
        else:
            self.updateCounter[packID-1] += 1

        # Atualiza o mostrador textBrowser_Buffer com as ultimas listas de dados recebidas.
        self.lastBuffers.writeLog(vectorToString(buffer, ' ', addNewLine=False))


    # Atualiza constantes com os valores lidos na interface
    def updateConstants(self):
        if self.ui.lineEdit_WheelPosMax.text() != '' and self.ui.lineEdit_WheelPosMin.text() != '':
            wheelPosMax = int(self.ui.lineEdit_WheelPosMax.text())
            wheelPosMin = int(self.ui.lineEdit_WheelPosMin.text())
            self.data.wheelPosMax = wheelPosMax
            self.data.wheelPosMin = wheelPosMin
            self.updateCounterMax[0] = int(self.ui.updateCounterP1.value())
            self.updateCounterMax[1] = int(self.ui.updateCounterP2.value())
            self.updateCounterMax[2] = int(self.ui.updateCounterP3.value())
            self.updateCounterMax[3] = int(self.ui.updateCounterP4.value())
            self.updateTime = self.ui.doubleSpinBox_UpdateTime.value() * 1000



    def updatePlot(self):
        # Só plotam gráfico da se a respectiva checkBox esta marcada pelo usuarios
        # Define as cores de cada gráfico
        # Os gráficos são compostos pelos últimos 50 pontos do dado
        # Arrasta vetor pto lado para que novo valor possa ser inserido

        # Atualiza graficos
        self.ui.graphicsView_EngineData.clear()
        if self.ui.checkBox_EngineTemperature.isChecked() == 1:
            self.ui.graphicsView_EngineData.plot(self.arrayTime3, self.arrayTemp, pen='r')
        if self.ui.checkBox_FuelPressure.isChecked() == 1:
            self.ui.graphicsView_EngineData.plot(self.arrayTime3, self.arrayFuelP, pen='g')
        if self.ui.checkBox_Voltage.isChecked() == 1:
            self.ui.graphicsView_EngineData.plot(self.arrayTime3, self.arrayBattery, pen='b')
        if self.ui.checkBox_OilPressure.isChecked() == 1:
            self.ui.graphicsView_EngineData.plot(self.arrayTime3, self.arrayOilP, pen='k')


    def update_diagramaGG(self):
    # atualiza o refcurso grafico DiagramaGG
        self.ui.graphicsView_DiagramaGG_DD_2.clear()
        self.ui.graphicsView_DiagramaGG_DD_2.plot([self.data.dic['acelX_DD']],
                                                [self.data.dic['acelY_DD']],
                                                pen=None,
                                                symbol='o')
        self.ui.graphicsView_DiagramaGG_DE_2.clear()
        self.ui.graphicsView_DiagramaGG_DE_2.plot([self.data.dic['acelX_DE']],
                                                [self.data.dic['acelY_DE']],
                                                pen=None,
                                                symbol='o')
        self.ui.graphicsView_DiagramaGG_TD.clear()
        self.ui.graphicsView_DiagramaGG_TD.plot([self.data.dic['acelX_TD']],
                                                [self.data.dic['acelY_TD']],
                                                pen=None,
                                                symbol='o')
        self.ui.graphicsView_DiagramaGG_TE.clear()
        self.ui.graphicsView_DiagramaGG_TE.plot([self.data.dic['acelX_TE']],
                                                [self.data.dic['acelY_TE']],
                                                pen=None,
                                                symbol='o')


    def updatePXInterface(self, n):
    # funcao que atualiza os valores da interface de acordo com o pacote recebido
        if self.ui.radioButton_applyFunctions.isChecked():
            dataDictionary = self.data.dic
        else:
            dataDictionary = self.data.dicRaw
        

        #PACOTE 1
        if n == 1:
                elements = len((self.data.packNames[0:18]))
                # Itera na variavel que contem a ordem dos pacotes para pegar as respectivas chaves do dicionario
                for key, i in zip((self.data.packNames[0:18]), range(0, elements)):
                    # Cria elemento da tabela, faz o alinhamento e coloca valor
                    item = QTableWidgetItem(str(dataDictionary[key]))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.ui.tableWidget_Package1.setItem(i, 0, item)
                    # Alarmes
                    if self.alarms.alarms[key] != []:
                        self.alarms.checkAlarm(key, self.ui.tableWidget_Package1, i)
                    else:
                        self.alarms.setFieldBackground(self.ui.tableWidget_Package1, self.alarms.white, i)
                self.update_diagramaGG()  # Chamada da função update_diagramagg

        #PACOTE 2
        if n == 2:
            elements = len((self.data.packNames[20:34]))
            for key, i in zip((self.data.packNames[20:34]), range(0, elements)):
                item = QTableWidgetItem(str(dataDictionary[key]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.ui.tableWidget_Package2.setItem(i, 0, item)

                #Alarmes
                if self.alarms.alarms[key] != []:
                        self.alarms.checkAlarm(key, self.ui.tableWidget_Package2, i)
                else:
                        self.alarms.setFieldBackground(self.ui.tableWidget_Package2, self.alarms.white, i)


            if ((self.data.dic['rearBrakeP'] + self.data.dic['frontBrakeP']) !=
                    0):  # Verificação necessária para que não ocorra divisão por zero
                self.ui.progressBar_FrontBrakeBalance.setValue(
                    100 * self.data.dic['frontBrakeP'] /
                    (self.data.dic['rearBrakeP'] + self.data.dic['frontBrakeP'])
                )  # porcentagem da pressão referente ao freio dianteiro
                self.ui.progressBar_RearBrakeBalance.setValue(
                    100 * self.data.dic['rearBrakeP'] /
                    (self.data.dic['rearBrakeP'] + self.data.dic['frontBrakeP']))  # traseiro

            # atualiza gauges
            self.ui.progressBar_FrontBreakPressure.setValue(self.data.dic['frontBrakeP'])
            self.ui.label_65.setText(str(self.data.dic['frontBrakeP']))
            self.ui.label_69.setText(str(self.data.dic['rearBrakeP']))
            # distribuicao dos freios
            self.ui.progressBar_RearBreakPressure.setValue(self.data.dic['rearBrakeP'])

            self.ui.progressBar_FuelPressure.setValue(self.data.dic['fuelP'])
            self.ui.label_17.setText(str(self.data.dic['fuelP']))

            self.ui.progressBar_OilPressure.setValue(self.data.dic['oleoP'])
            self.ui.label_10.setText(str(self.data.dic['oleoP']))

            self.ui.progressBar_TPS.setValue(self.data.dic['tps'])
            self.ui.progressBar_TPS.setProperty("value", self.data.dic['tps'])

            self.ui.dial_WheelPos.setValue(self.data.dic['volPos'])
            self.ui.label_19.setText(str(self.data.dic['volPos']))

            self.updatePlot()

        #PACOTE 3
        if n ==3:
            elements = len((self.data.packNames[35:52]))
            for key, i in zip((self.data.packNames[35:52]), range(0, elements)):
                item = QTableWidgetItem(str(dataDictionary[key]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.ui.tableWidget_Package3.setItem(i, 0, item)

                if self.alarms.alarms[key] != []:
                        self.alarms.checkAlarm(key, self.ui.tableWidget_Package3, i)
                else:
                    self.alarms.setFieldBackground(self.ui.tableWidget_Package3, self.alarms.white, i)


            # Gauge da bateria
            self.ui.progressBar_BatteryVoltage.setValue(int(self.data.dic['batVoltage']))
            self.ui.label_15.setText(str(self.data.dic['batVoltage']))

            self.ui.progressBar_EngineTemperature.setValue(self.data.dic['ect'])
            self.ui.label_6.setText(str(self.data.dic['ect']))

            if (int(self.data.dicRaw['releVent']) == 1):
                self.ui.radioButton_FanRelay.setChecked(False)
            else:
                self.ui.radioButton_FanRelay.setChecked(True)

            if (int(self.data.dicRaw['releBomba']) == 1):
                self.ui.radioButton_FuelPumpRelay.setChecked(False)
            else:
                self.ui.radioButton_FuelPumpRelay.setChecked(True)

            self.updatePlot()

        #PACOTE 4
        if n == 4:
            elements = len((self.data.packNames[53:65]))
            for key, i in zip((self.data.packNames[53:65]), range(0, elements)):
                item = QTableWidgetItem(str(dataDictionary[key]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.ui.tableWidget_Package4.setItem(i, 0, item)

                #Alarmes
                if self.alarms.alarms[key] != []:
                        self.alarms.checkAlarm(key, self.ui.tableWidget_Package4, i)
                else:
                        self.alarms.setFieldBackground(self.ui.tableWidget_Package4, self.alarms.white, i)
