import PyQt5
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets


class Setup:
    def __init__(self, ui, errorLog, alarms, settings):
        self.ui = ui   # instancia grafica 
        self.log = errorLog      # instancia de Log()
        self.alarms= alarms # instancia de Alarms()
        self.settings = settings # settings armazena os campos de configuracao na interface


    # Salva os valores do Setup atual
    def saveSetup(self):
        self.settings.setValue('wheelPosMax', str(self.ui.lineEdit_WheelPosMax.text()))
        self.settings.setValue('wheelPosMin', str(self.ui.lineEdit_WheelPosMin.text()))
        self.settings.setValue('calibConstant', str(self.ui.lineEdit_CalibrationConstant.text()))
        self.settings.setValue('setupCar', str(self.ui.lineEdit_SetupCar.text()))
        self.settings.setValue('setupTrack', str(self.ui.lineEdit_SetupTrack.text()))
        self.settings.setValue('setupDriver', str(self.ui.lineEdit_SetupDriver.text()))
        self.settings.setValue('setupTemp', str(self.ui.lineEdit_SetupTemperature.text()))
        self.settings.setValue('setupAntiroll', str(self.ui.lineEdit_SetupAntiroll.text()))
        self.settings.setValue('tirePFront', str(self.ui.lineEdit_SetupTirePressureFront.text()))
        self.settings.setValue('tirePRear', str(self.ui.lineEdit_SetupTirePressureRear.text()))
        self.settings.setValue('aeroAngle', str(self.ui.lineEdit_SetupWingAttackAngle.text()))
        self.settings.setValue('engineMap', str(self.ui.lineEdit_SetupEngineMap.text()))
        self.settings.setValue('balanceBar', str(self.ui.lineEdit_SetupBalanceBar.text()))
        self.settings.setValue('setupDrexler', str(self.ui.lineEdit_SetupDifferential.text()))
        self.settings.setValue('setupComments', str(self.ui.textEdit_SetupComments.toPlainText()))
        self.settings.setValue('filename', self.ui.lineEdit_FileName.text())
        self.settings.setValue('sampleRate1', self.ui.lineEdit_SampleRate1.text())
        self.settings.setValue('sampleRate2', self.ui.lineEdit_SampleRate2.text())
        self.settings.setValue('sampleRate3', self.ui.lineEdit_SampleRate3.text())
        self.settings.setValue('sampleRate4', self.ui.lineEdit_SampleRate4.text())


    #Carrega os valores de Setup salvos
    def loadSetup(self):
        # Primeira verificação e tratamento de exceção
        try:
            filename = self.settings.value('filename')
            self.ui.lineEdit_FileName.setText(filename)
        except:
            self.errorLog.writeLog("Erro ao carregar config do arquivo")

        # Segunda verificação e tratamento de exceção
        try:
            self.ui.textEdit_SetupComments.setText(self.settings.value('setupComments'))
            self.ui.lineEdit_WheelPosMax.setText(self.settings.value('wheelPosMax'))
            self.ui.lineEdit_WheelPosMin.setText(self.settings.value('wheelPosMin'))
            self.ui.lineEdit_CalibrationConstant.setText(self.settings.value('calibConstant'))
            self.ui.lineEdit_SetupCar.setText(self.settings.value('setupCar'))
            self.ui.lineEdit_SetupTrack.setText(self.settings.value('setupTrack'))
            self.ui.lineEdit_SetupDriver.setText(self.settings.value('setupDriver'))
            self.ui.lineEdit_SetupTemperature.setText(self.settings.value('setupTemp'))
            self.ui.lineEdit_SetupAntiroll.setText(self.settings.value('setupAntiroll'))
            self.ui.lineEdit_SetupTirePressureFront.setText(self.settings.value('tirePFront'))
            self.ui.lineEdit_SetupTirePressureRear.setText(self.settings.value('tirePRear'))
            self.ui.lineEdit_SetupWingAttackAngle.setText(self.settings.value('aeroAngle'))
            self.ui.lineEdit_SetupEngineMap.setText(self.settings.value('engineMap'))
            self.ui.lineEdit_SetupBalanceBar.setText(self.settings.value('balanceBar'))
            self.ui.lineEdit_SetupDifferential.setText(self.settings.value('setupDrexler'))
            self.ui.textEdit_SetupComments.setText(self.settings.value('setupComments'))
            self.ui.lineEdit_SampleRate1.setText(self.settings.value('sampleRate1'))
            self.ui.lineEdit_SampleRate2.setText(self.settings.value('sampleRate2'))
            self.ui.lineEdit_SampleRate3.setText(self.settings.value('sampleRate3'))
            self.ui.lineEdit_SampleRate4.setText(self.settings.value('sampleRate4'))

        except:
            self.log.writeLog("Erro ao carregar configs")
        '''
        # Terceira verificação e tratamento de exceção para alarmes
        try:
            i=0
            for key in self.alarms.alarms:
                if self.settings.contains('alarm'+key):
                    print(i)
                    i+=1
                    store = self.settings.value('alarm'+key)
                    print(store[0])
                    print(store[1])
                    print(store[2])
                    if (store[0] != '' and store[1] == ''):
                        store[0] = float(store[0])
                        store[1] = ''
                    elif (store[0] == '' and store[1] != ''):
                        store[0] = ''
                        store[1] = float(store[1])
                    else:
                        store[0] = float(store[0])
                        store[1] = float(store[1])

                    self.alarms.alarms[key] = store
        except:
            self.log.writeLog("Erro ao carregar config de alarme")

        
        # Quarta verificação e tratamento de exceção para o hodometro
        try:


        except:
            self.log.writeLog("Erro ao carregar config do hodometro")
        '''
