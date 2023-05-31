# This Python file uses the following encoding: utf-8
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtCore import pyqtSignal as Signal

import utils.os_utils as OsUtils

from window import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):

    instructions_loaded = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.setWindowTitle('Simulador do Algoritmo de Tomasulo')
        self.showMaximized()
        self.stepButton.setEnabled(False)

    #@pyQtSlot
    def load_instructions_from_system(self):

        if self.instructionsScroll.tomasulo != None:

            msg = QMessageBox()

            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("A simulação se encontra em progresso. Deseja continuar?")
            msg.setInformativeText("Clique em \'Ok\' para progredir, e \'Cancel\' para continuar na simulação atual")
            msg.setWindowTitle("Simulação em Progresso")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            msg.setDefaultButton(QMessageBox.StandardButton.Ok)

            resp = msg.exec()

            if resp == QMessageBox.StandardButton.Cancel:
                return

            self.instructionsList.clean_instructions()

        file_path = QFileDialog.getOpenFileName(
                    self,
                    str("Abrir instruções"),
                    OsUtils.get_user_home(),
                    filter="Arquivos de texto (*.txt)")[0]

        if not file_path:
            return 

        self.stepButton.setEnabled(True)

        self.instructions_loaded.emit(file_path)

    #@pyQtSlot
    def tomasulo_finalized(self):
        self.instructionsList.clean_instructions()
        self.stepButton.setEnabled(False)



if __name__ == "__main__":

    qt_app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(qt_app.exec())
