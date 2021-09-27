# Escreve mensagens na instancia logInstance.
# Utilizada para escrita de campos com muito texto na interface, no caso, imprime mensagens ao usuário
class Log:
    def __init__(self, logInstance, ui, maxElements):
        self.Log = []
        self.logInstance = logInstance
        self.maxElements = maxElements
        self.on = 'off'
        self.ui = ui

    # Insere novo texto de erro na primeira posicao do vetor
    def writeLog(self, text):
        if self.on == 'off':
            return
        
        self.Log.append(" ")
        # Faz o roll (Arrasta dados, apagando a informação mais antiga e subtituindo pela mais recente)
        if len(self.Log) < self.maxElements:
            self.Log = self.Log[-1:] + self.Log[:-1]
            self.Log[0] = text
        else:
            self.Log = self.Log[-1:] + self.Log[:self.maxElements-1]
            self.Log[0] = text
        string = '\n'.join(str(x) for x in self.Log)
        self.logInstance.setText(string)


    # Verifica se opções de exibição de logs de error ou buffer de dados estão habilitados pelo usuário
    def logEnabled(self, buffer_or_error):
        if buffer_or_error == "error":
            if self.ui.radioButton_errorLog.isChecked():
                self.on = 'on'
            else:
                self.on = 'off'

        if buffer_or_error == "buffer":
            if self.ui.radioButton_bufferLog.isChecked():
                self.on = 'on'
            else:
                self.on = 'off'
