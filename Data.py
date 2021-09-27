#Pacote importado
import copy

#* Classe que processa e armazena dados atuais em dicionários
class Data:
    #*Construtor
    def __init__(self, ui):
        self.ui= ui

        # Constantes
        self.wheelPosMax = 0
        self.wheelPosMin = 0
        self.pSizes = [18, 35, 36, 47]  # número de bytes de cada pacote
        
        # Dicionários com 'identificadores' (chaves) para todos os dados dos 4 pacotes em ordem
        self.dic = {
            'acelX': 0, 'acelY': 0, 'acelZ': 0, 
            'velAN': 0, 'velDD': 0, 'velDE': 0, 'velTD': 0, 'velTE': 0, 'rpm': 0, 'beacon': 0, 'time': 0, 'hodometro': 0,

            'ext1': 0, 'ext2': 0, 'ext3': 0, 'ext4': 0, 'ext5': 0, 'ext6': 0, 'ext7': 0, 'ext8': 0, 'ext9': 0, 'ext10': 0,
            'time2': 0,
            
            'tps': 0, 'oleoP': 0, 'fuelP': 0, 'injectors': 0, 'suspDD': 0, 'suspDE': 0, 'suspTD': 0, 'suspTE': 0,
            'volPos': 0, 'correnteBat': 0, 'correnteVent': 0, 'correnteBomba': 0, 'rearBrakeP': 0, 'frontBrakeP': 0, 'time3': 0,

            'batVoltage': 0, 'ect': 0, 'oilTemp': 0, 'tempDiscoDD': 0, 'tempDiscoDE': 0, 'tempDiscoTD': 0, 'tempDiscoTE': 0,
            'tempVent': 0, 'tempBomba': 0, 'releVent': 0, 'releBomba': 0, 'mata': 0, 'gpsLat': 0, 'gpsNS': 0, 'gpsLong': 0,
            'gpsEW': 0, 'gpsData':0, 'gpsHora':0,'sparkCut':0,'tempBat': 0,'runners': 0, 'time4': 0,

        }
        # Dicionário cru
        self.dicRaw = copy.deepcopy(self.dic)

        # Dicionário utilizado para chamada do método "updatePnData", sendo n o número do pacote 
        self.updateDataFunctions = {1: self.updateP1Data, 2: self.updateP2Data, 3: self.updateP3Data, 4: self.updateP4Data}

        # Hodometro, dicionário com nome e metragem da volta, de pistas padrões
        self.pistas = {'Selecione uma pista': 0, 'Kartodromo Betim': 1100, 'Enduro': 1000}

        #Lista com as chaves do dicionarios dic, isso é, o nome dos dados dos 4 pacotes
        self.packNames= list(self.dic.keys()) 



    #*METÓDOS    

    #* Atualiza os campos na parte de "Odometer" da interface.
    #* É chamado quando o usuario escolhe algum dado no comboBox "trackOdometer"
    def displayTracks(self):
        text = self.ui.trackOdometerComboBox.currentText()
        track = self.pistas[text]
        if track != []:
            self.ui.distanceTracklineEdit.setText(str(track))
        else:
            self.ui.distanceTracklineEdit.setText('')


    #* Salva nova pista configurada pelo usuário
    def saveTrack(self):
        # associar campos das interfaces às variáveis
        track = self.ui.trackOdometerComboBox.currentText()
        if track == 'Selecione uma pista':
            nameTrack = str(self.ui.nameTracklineEdit_2.text()) #texto de New Track - deverá ser uma nova chave no dicionário
            valTrack = float(self.ui.distanceTracklineEdit.text()) #texto de Track Distance - deverá ser o valor da da chave do dicionário
            self.pistas[nameTrack] = valTrack #adiciona nova pista no dicionário
        
        # atualiza a ComboxBox de pista
        self.ui.trackOdometerComboBox.clear()
        self.ui.trackOdometerComboBox.addItems(self.pistas)
        self.ui.nameTracklineEdit_2.setText('')
        self.ui.distanceTracklineEdit.setText('')


    #* Para valores do tipo signed, esse método os trata com complemento de 2
    #* Usado para os dados de aceleração
    def twosComplement(self, number, bits):
        if (number & (1 << (bits - 1))) != 0:
            number = number - (1 << bits) # computa valores negativos
        return number


    #* Processamento e armazenamento do Pacote 1
    def updateP1Data(self, buffer):
        if ((int(buffer[0]) == 1) and (len(buffer) == self.pSizes[0])):  # Testa se é o pacote 1 e se está completo.
            
            # Acelerometros
            for i in range(0, 4):
                j = 2 + 2*i
                p1 = (self.packNames[0:10])
                key = p1[i]                
                self.dicRaw[key] =  (buffer[j] << 8) + buffer[j+1] 
                self.dicRaw[key] = self.twosComplement(self.dicRaw[key], 16) # Complemento de 2
                self.dic[key] = round(float(self.dicRaw[key] / 16384), 3) 
            
            # Velocidade das 4 rodas, Rpm, beacon e tempo do pacote
            self.dicRaw['velDD'] = int(buffer[10])
            self.dicRaw['velDE'] = int(buffer[11])
            self.dicRaw['velTD'] = int(buffer[12])
            self.dicRaw['velTE'] = int(buffer[13])
            self.dicRaw['rpm'] = (int(buffer[14]) << 8) + int(buffer[15])
            self.dicRaw['beacon'] = int(buffer[16])
            self.dicRaw['time'] = ((buffer[17]) << 8) + int(buffer[18])
            
            # Dados que não precisam de processamento
            self.dic['velDE'] = self.dicRaw['velDE']
            self.dic['velDD'] = self.dicRaw['velDD']
            self.dic['velTE'] = self.dicRaw['velTE']
            self.dic['velTD'] = self.dicRaw['velTD']
            self.dic['rpm'] = self.dicRaw['rpm']
            self.dic['beacon'] = self.dicRaw['beacon']

            # Beacon e Hodometro
            if(self.dic['beacon'] != 0):
                self.dic['hodometro'] += self.pistas[self.ui.trackOdometerComboBox.currentText()]

            self.dic['time'] = 25 * self.dicRaw['time']
            return 1    

        else:
            return 0

    #* Processamento e armazenamento do Pacote 2
    #* Somente dados de extensometria, tratamentos mais simples, por ser um unica tipo de dado
    def updateP2Data(self, buffer):
        if ((int(buffer[0]) == 2) and (len(buffer) == self.pSizes[1])):  # testa se é o pacote 2 e se está completo
            p2 = (self.packNames[12:22])
            for i in range(0, len(p2) -1):
                j = 2 + 3*i
                key = p2[i]
                self.dicRaw[key] = (buffer[j] << 16) + (buffer[j+1] << 8) + buffer[j+2]
                self.dic[key] = self.dicRaw[key]
            self.dicRaw['time2'] = (buffer[32] << 8) + (buffer[33])
            self.dic['time2'] = 25 * self.dicRaw['time2']
            return 1
        else:
            return 0

    #* Processamento e armazenamento do Pacote 3
    def updateP3Data(self, buffer):
        if ((int(buffer[0]) == 3) and (len(buffer) == self.pSizes[2])):  #Testa se é o pacote 3 e se está completo

            #. Todos os dados do pacote 3 sao no formato byte1 << 8 | byte2 
            # Se realiza soma dos 2bytes para cada dado e armazena em dicRaw
            p3 = (self.packNames[23:37])
            for i in range(0, len(p3)):
                j = 2 + 2*i   
                key = p3[i]                
                self.dicRaw[key] =  (buffer[j] << 8) + buffer[j+1]

            # Processamento dos dados
            self.dic['tps'] = 0.1*self.dicRaw['tps']
            self.dic['oleoP'] = round(float(self.dicRaw['oleoP'] * 0.001), 4)
            self.dic['fuelP'] = round(float(self.dicRaw['fuelP'] * 0.001), 4)
            self.dic['rearBrakeP'] = round(self.dicRaw['rearBrakeP'] * 0.02536, 2)
            self.dic['frontBrakeP'] = round(self.dicRaw['frontBrakeP'] * 0.02536, 2)
            
            #Valores de wheelPosMax e wheelPosMin são constantes definidas pelo usuário na interface
            if self.wheelPosMax - self.wheelPosMin != 0:
                self.dic['volPos'] = round(((self.dicRaw['volPos'] - self.wheelPosMin) * 240 / (self.wheelPosMax - self.wheelPosMin) - 120), 2)
            
            self.dic['injectors'] = self.dicRaw['injectors']
            self.dic['correnteBat'] = round(self.dicRaw['correnteBat'] * 0.014652, 3) - 29.3
            self.dic['suspDE'] = self.dicRaw['suspDE']
            self.dic['suspDD'] = self.dicRaw['suspDD']
            self.dic['suspTE'] = self.dicRaw['suspTE']
            self.dic['suspTD'] = self.dicRaw['suspTD']
            self.dic['correnteVent'] = self.dicRaw['correnteVent']
            self.dic['correnteBomba'] = self.dicRaw['correnteBomba']
            self.dic['time3'] = 25 * self.dicRaw['time3']
            return 1
        
        else:
            return 0


    #* Processamento e armazenamento do Pacote 4
    def updateP4Data(self, buffer):
        if ((int(buffer[0]) == 4) and (len(buffer) == self.pSizes[3])):  #Testa se é o pacote 4 e está completo

            # os 10 primeiros dados sao no formato byte1 <<8 | byte2
            for i in range(0, 10):
                j = 2 + 2*i
                p4 = (self.packNames[38:59])
                key = p4[i]                
                self.dicRaw[key] =  (buffer[j] << 8) + buffer[j+1]
            
            # Dados que ocupam mais de 2 bytes, sendo somados e atribuidos em dicRaw
            self.dicRaw['releBomba'] = int((buffer[22] & 128) >> 7)
            self.dicRaw['releVent'] = int((buffer[22] & 8) >> 3)
            self.dicRaw['mata'] = int((buffer[22] & 32) >> 5)
            self.dicRaw['gpsLat'] = (buffer[23] << 16) + (buffer[24] << 8) + buffer[25]
            self.dicRaw['gpsLong'] = (buffer[26] << 16) + (buffer[27] << 8) + buffer[28]
            self.dicRaw['gpsNS'] = int(buffer[29])
            self.dicRaw['gpsEW'] = int(buffer[30])
            self.dicRaw['time4'] = (buffer[38] << 8) + buffer[39]

            '''Falta gps hora, minuto, segundo, ms, ano, mes dia nessa ordem
            #Tschaen, fazer chamada para função do GPS'''

            #Processamento dos dados
            self.dic['batVoltage'] = round(float(self.dicRaw['batVoltage'] * 0.01), 2)
            self.dic['ect'] = round(float(self.dicRaw['ect'] * 0.1), 2)
            self.dic['oilTemp'] = self.dicRaw['oilTemp']
            self.dic['tempDiscoDD'] = round(float(self.dicRaw['tempDiscoDD']), 2)
            self.dic['tempDiscoDE'] = round(float(self.dicRaw['tempDiscoDE']), 2)
            self.dic['tempDiscoTD'] = round(float(self.dicRaw['tempDiscoTD']), 2)
            self.dic['tempDiscoTE'] = round(float(self.dicRaw['tempDiscoTE']), 2)
            self.dic['tempVent'] = self.dicRaw['tempVent']
            self.dic['tempBomba'] = self.dicRaw['tempBomba']
            self.dic['releVent'] = 'ON' if self.dicRaw['releVent'] == 1 else 'OFF'
            self.dic['releBomba'] = 'ON' if self.dicRaw['releBomba'] == 1 else 'OFF'
            self.dic['mata'] = 'ON' if self.dicRaw['mata'] == 1 else 'OFF'
            self.dic['gpsLat'] = self.dicRaw['gpsLat']
            self.dic['gpsNS'] = self.dicRaw['gpsNS']
            self.dic['gpsLong'] = self.dicRaw['gpsLong']
            self.dic['gpsEW'] = self.dicRaw['gpsEW']
           
            self.dic['gpsData'] = self.dicRaw['gpsData']
            self.dic['gpsHora'] = self.dicRaw['gpsHora']
           
            self.dic['sparkCut'] = self.dicRaw['sparkCut']
            self.dic['tempBat'] = self.dicRaw['tempBat']
           
            self.dic['runners'] = self.dicRaw['runners']
            self.dic['time4'] = 25 * self.dicRaw['time4']
            return 1
        
        else:
            return 0
    

