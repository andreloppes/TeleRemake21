#Pacotes importados
import PyQt5
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets

import copy

#Classe importadas
from Data import Data

# Classe responsável por todas operações que envolvem alarmes.
class Alarms:
    #Construtor
    def __init__(self, data, ui, settings):
        self.data = data    #Instancia da classe Data
        self.ui = ui        #Instancia gráfica
        self.settings= settings
        #Atributos
        self.alarms = copy.deepcopy(self.data.dic)    #dicionário de alarms
        self.alarmTypes = ['', 'greater than', 'lesser than', 'equal to']    #tipos de alarmes

        #cores do tipo QtGui.QColor(r, g, b)
        self.white= QtGui.QColor(255, 255, 255)
        self.red= QtGui.QColor(255, 0, 0)
        self.yellow= QtGui.QColor(255, 255, 0)


    #* MÉTODOS

    #* Reseta os alarmes padrões
    def setDefaultAlarms(self):
        #apaga todos alarmes configurados até então na interface
        for key in self.alarms:
            self.alarms[key] = []
            if self.settings.contains('alarm'+key):
                self.settings.remove('alarm'+key)

        #reseta os alarmes padrões com valores pré-configurados 
        self.alarms['batVoltage'] = [12.0, 14.0, 'lesser than'] 
        self.alarms['ect'] = [80.0, 90.0, 'greater than']
        self.alarms['tempDiscoDE']=['',100.0, 'greater than']
        self.alarms['tempDiscoDD']=['',100.0, 'greater than']
        self.alarms['tempDiscoTE']=['',100.0, 'greater than']
        self.alarms['tempDiscoTD']=['',100.0, 'greater than']
        self.alarms['oilTemp']=['',3.0, 'equal to']
        self.alarms['oleoP']=['',1.0, 'greater than']
        self.displayAlarm()


    #* Salva alarme configurado pelo usuário
    def saveAlarm(self):
        #associa campos da interface a variaveis
        key = self.ui.alarmComboBox.currentText()
        type = self.ui.alarmTypeComboBox.currentText()
        valWorring = self.ui.alarmlineEdit.text()
        valCritical = self.ui.alarmlineEdit_2.text()
        
        #Salva alarme com novos valores configurados
        
        #caso não tenha inserido o tipo do alarme, ele não é salvo
        if (type == ''):
            if self.settings.contains('alarm'+key):
                self.settings.remove('alarm'+key)
                self.alarms[key] = []
        
        #salva alarme somente com valor preocupante inserido
        elif (valWorring != '' and valCritical == ''):
            store = [float(valWorring),'', type]
            self.settings.setValue('alarm' + key, store)
            self.alarms[key] = store
            self.displayAlarm()
        
        #salva alarme somente com valor critico inserido
        elif (valWorring == '' and valCritical != ''):
            store = ['',float(valCritical), type]
            self.settings.setValue('alarm' + key, store)
            self.alarms[key] = store
            self.displayAlarm()
        
        #salva alarme com os dois valores inserido-
        else:
            store = [float(valWorring),float(valCritical), type]
            self.settings.setValue('alarm' + key, store)
            self.alarms[key] = store
            self.displayAlarm()


    #* Atualiza os campos na parte de configuracao dos alarmes.
    #* É chamado quando o usuario escolhe algum dado no comboBox dos alarmes
    def displayAlarm(self):
        # Pega qual dado esta selecionado no combobox e acessa no dicionario alarms
        text = self.ui.alarmComboBox.currentText()
        val = self.alarms[text]

        # Caso o alarme exista, mostra ele no campo, com seu tipo e valores (worring e critical)
        if val != []:
            self.ui.alarmlineEdit.setText(str(val[0]))
            self.ui.alarmlineEdit_2.setText(str(val[1]))
            index = self.alarmTypes.index(val[2])
            self.ui.alarmTypeComboBox.setCurrentIndex(index)
        else:
            self.ui.alarmlineEdit.setText('')
            self.ui.alarmlineEdit_2.setText('')
            self.ui.alarmTypeComboBox.setCurrentIndex(0)


    #* Colore o background do dado na lista da interface na cor color
    def setFieldBackground(tableWidget, color, i):
        for j in range(0, 2):
            item = tableWidget.item(i, j)
            item.setBackground(color) #cor(r,b,b)


    #* Verifica se alarme configurado deve ser disparado, comparando com o valor armazenado em data.dic
    def checkAlarm(self, key, tableWidget, i):
        worring = self.alarms[key][0]
        critical= self.alarms[key][1]
        type = self.alarms[key][2]
        
        #para alarmes 'maior que'
        if type == 'greater than':
            if self.data.dic[key] > critical:
                self.setFieldBackground(tableWidget, self.red, i)
            elif worring != '':
                if self.data.dic[key] > worring:
                    self.setFieldBackground(tableWidget, self.yellow, i)
            else:
                self.setFieldBackground(tableWidget, self.white, i)

        #para alarmes 'menor que'
        elif type == 'lesser than':
            if self.data.dic[key] < critical:
                self.setFieldBackground(tableWidget, self.red, i)
            elif worring != '':
                if self.data.dic[key] < worring:
                    self.setFieldBackground(tableWidget, self.yellow, i)
            else:
                self.setFieldBackground(tableWidget, self.white, i)

        #para alarmes 'igual a'
        elif type == 'equals':
            if worring != '' and critical != '':
                if self.data.dic[key] == worring or self.data.dic[key] == critical:
                    self.setFieldBackground(tableWidget, self.red, i)
                else:
                    self.setFieldBackground(tableWidget, self.white, i)
