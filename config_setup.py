#!/usr/bin/env python3
#
# Author : Nikhil Nayak (nikhil.nixel@gmail.com)
# Usage  : .py
#
import sys, os
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication
print("[ OK ] - Config INIT.")
app_ = QApplication([])
Ui_MainWindow, QtBaseClass = uic.loadUiType("UI/config_ui.ui")  # specify the location of your .ui file
print("[ OK ] - Loaded UI.")


class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.config_dir = "BLU UserDATA/"
        self.ui.submitButton.pressed.connect(self.on_submit)
        try:
            os.mkdir(self.config_dir)
        except FileExistsError:
            pass

    def on_submit(self):
        if '' in (self.ui.lineEdit.displayText(), self.ui.lineEdit_2.displayText()):
            return None
        with open(self.config_dir + 'UserInf0.config', 'w+') as f:
            textbox1_text = self.ui.lineEdit.displayText().title()
            f.write('<#fname#>=' + textbox1_text + '\n')
            f.write('<#uname#>=' + textbox1_text.split(' ')[0] + '\n')
            f.write('<#emailID#>=' + self.ui.lineEdit_2.displayText())

        self.close()


def run_config_setup():
    window_ = MyApp()
    window_.setWindowIcon(QIcon('IMAGES/BLU-LOGO.png'))
    window_.setWindowFlags(Qt.FramelessWindowHint)
    window_.setWindowTitle('BLU | VI | Config')
    window_.show()
    app_.exec()


if __name__ == "__main__":
    run_config_setup()
