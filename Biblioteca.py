import PyQt5
from PyQt5.QtWidgets import QMessageBox


# Retirar desse arquivo e implementar em bibliotecas assim como objetivo com funções do main
# Concatena vetor em uma string separada por delimiter
def vectorToString(line, delimiter, addNewLine=True):
    string = delimiter.join(str(x) for x in line)
    if addNewLine:
        string = string + '\n'
    return string


# Exibe mensagens de erro na tela
def displayErrorMessage(text):
    dlg = QMessageBox(None)
    dlg.setWindowTitle("Error!")
    dlg.setIcon(QMessageBox.Warning)
    dlg.setText(
    "<center>" + text + "<center>")
    dlg.exec_()
