#
# Author : Nikhil Nayak (nikhil.nixel@gmail.com)
# Usage  : .py
# 


from functools import partial
from urllib.request import urlretrieve
from math import cos, pi
from PyQt5 import uic
from PyQt5.QtCore import Qt, QSize, QThreadPool, pyqtSlot, QObject, QRunnable, QTimer, QPoint, QEvent
from PyQt5.QtGui import QMovie, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QTextEdit

import os, sys, time
import _thread

# USER DATA CREATION
from config_setup import run_config_setup
if not os.path.isfile('BLU UserDATA/UserInf0.config'):
    run_config_setup()
##

# IMPORTING CORE MODULES
from CORE.RESPONSE_NET import respond_text
from CORE.UTILS import sweep_dir
from CORE.TTS import say
from CORE.STT import listen_and_decode
##
print("[ OK ] - Libraries Imported")
app = QApplication([])
ScreenSizeObject = QDesktopWidget().screenGeometry(-1)  # Screen Attribute Bucket(or Object)
Ui_MainWindow, QtBaseClass = uic.loadUiType("UI/action_tab.ui")  # Specify the location of your .ui file here!


class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.loading_animate = QMovie('IMAGES/GIFS/load_resp.gif')
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setGeometry(
            ScreenSizeObject.width()-self.width()-10,
            ScreenSizeObject.height()-self.height(),
            self.width(),
            self.height()
        )

        self.original_height = self.height()
        self.original_pos_height = self.pos().y()
        self.ui.text_original_height = self.ui.textDisplay.height()
        self.ui.queryBox.returnPressed.connect(self.load_response)
        self.ui.speechRecog.clicked.connect(self.load_response_stt)
        self.ui.textDisplay.setLineWrapMode(QTextEdit.NoWrap)
        self.installEventFilter(self)

        time_frame_values = [i/30 for i in range(30)]  # Stores Animation Time frame for smooth Enlarging of window!!
        self.timeFrame = list(map(lambda x: x**0.5, time_frame_values))  # Time frame Values Producing Ease out Effect by using SQRT(type:func)

    def start_loader(self):
        """
        This Function displays an animated LOADING gif image during the processing session of this application,
        Starts when RETURN KEY is pressed!
        &&
        Clean wipes the folder containing the temporary images fetched during previous Query Session!
        """
        self.loading_animate.setScaledSize(QSize(400, 300))
        self.ui.loader.setMovie(self.loading_animate)
        self.loading_animate.setSpeed(200)
        self.ui.loader.show()
        self.loading_animate.start()
        sweep_dir("DATA-FOLDER/Temporary Fetched Images")

    @pyqtSlot()
    def stop_loader(self):
        """
        This function is called when all the data is fetched for Display.

        Q: WHAT IT DOES?
        A: Hides the loading gif Animation and slowly moves the window Upward with EASE-OUT effect!
           (Probably for displaying enlarged view of results)
        """
        self.ui.loader.hide()
        self.loading_animate.stop()

        if self.original_pos_height != self.pos().y():
            return

        for i in self.timeFrame:
            self.move(QPoint(ScreenSizeObject.width()-self.width()-10, ScreenSizeObject.height()-self.original_height-(i*300)))
            # WTS HAPPENED HERE
            time.sleep(0.005)

        self.resize(QSize(self.width(), self.original_height + 300))
        self.ui.textDisplay.resize(QSize(self.ui.textDisplay.width(), self.ui.text_original_height + 270))

    def eventFilter(self, obj, event):
        """
        If you dare click out of this window! Then the consequences are:
            self.on_focus_out()->CALLED
        """
        if event.type() == QEvent.WindowDeactivate:
            QTimer.singleShot(0, self.on_focus_out)

        return False

    def on_focus_out(self):
        """
        This function slides down MainWindow with EASE-OUT effect!
        And it is called only when you dare to click else where except MainWindow.
        """
        print("Focus Out!!")  # DON'T BOTHER (DEBUGGING $#!+)
        if self.original_height == self.height():
            print("Already MINIMUM")  # DON'T BOTHER (DEBUGGING $#!+)
            return

        for i in reversed(self.timeFrame):
            self.move(QPoint(ScreenSizeObject.width()-self.width()-10, ScreenSizeObject.height() -
                             self.original_height-(i * 300)))
            time.sleep(0.005)

        self.ui.textDisplay.resize(QSize(self.ui.textDisplay.width(), self.ui.text_original_height))
        self.resize(QSize(self.width(), self.original_height))

    def get_response(self, text):
        """
        I believe, you are clever enough to understand what it does! Don't Ya!

        Well, if you don't, follow these steps below:
            Step #1: Slap that pretty face of yours to wipe that grin off your cheek!
            Step #2: Rub your eyes clean!
            Step #3: Get ready for what I have to say next!

                    NOW, IMAGINE A FUNCTION THAT TAKES TEXT INPUT AND INSERTS THE RESULT IN THE TEXT-BROWSER, ALONG WITH
                    SPEECH!
        """
        if text[0] == "ERROR":
            plain_text, speech = [text[1]]*2
            speech = speech[0]
        else:
            plain_text, speech = respond_text(str(text))

        QTimer.singleShot(0, self.stop_loader)
        for pod in plain_text:
            if pod.split('─\n')[-1].startswith('https://'):
                fname = 'DATA-FOLDER/Temporary Fetched Images/temp_'+str(hash(pod))+'.jpg'
                if not os.path.exists('DATA-FOLDER/Temporary Fetched Images/'):
                    os.mkdir('DATA-FOLDER/Temporary Fetched Images/')
                urlretrieve(pod.split('─\n')[-1], fname)  # Store Image in temporary location
                wrapper = partial(self.ui.textDisplay.insertPlainText, pod.split('─\n')[0] + '─\n')  # Heading
                QTimer.singleShot(0, wrapper)
                wrapper = partial(self.ui.textDisplay.insertHtml, "<div style=\"border-radius: 50%;\" ><img src=\"" + fname + "\" /></div><br/><br/><br/>")   # Image URL
                QTimer.singleShot(0, wrapper)
            else:
                if '│' not in pod:
                    pod = pod.replace('─\n', '─-')\
                          .replace('\n─', '-─')\
                          .replace('\n', '.\n')\
                          .replace('─-', '─\n')\
                          .replace('-─', '\n─')\
                          .replace('  ', ' ')

                    pline = ''
                    max_len_wrap = 60  # Wrapping after exceeding the 'n' characters

                    for i in range(len(pod)):
                        pline += pod[i]

                        if (pod[i] == ' ') and (len(pline.split('\n')[-1]) > max_len_wrap):
                            pline += '\n'

                    pod = pline

                wrapper = partial(self.ui.textDisplay.insertPlainText, pod + '\n\n\n')
                QTimer.singleShot(0, wrapper)

        if speech == '':
            say("Here you GO!")
        else:
            say(speech)

    def load_response(self):
        """
        Wipes clean the TextBrowser and calls self.get_response() in separate thread!
        """
        self.ui.textDisplay.setText('')
        self.start_loader()
        self.resize(QSize(self.width(), self.original_height + 300))
        self.ui.textDisplay.resize(QSize(self.ui.textDisplay.width(), self.ui.text_original_height + 300))
        text = self.ui.queryBox.displayText()
        _thread.start_new_thread(self.get_response, (text,))

    def load_response_stt(self):
        """
        Wipes clean the TextBrowser and calls self.get_response() in separate thread!
        """
        self.ui.textDisplay.setText('')
        self.ui.queryBox.setText('')
        self.start_loader()
        self.resize(QSize(self.width(), self.original_height + 300))
        text = listen_and_decode()  # self.ui.queryBox.displayText()
        if text[0] != "ERROR":
            self.ui.queryBox.setText(text)

        _thread.start_new_thread(self.get_response, (text,))


if __name__ == '__main__':
    window = MyApp()
    window.setWindowFlags(Qt.FramelessWindowHint)
    window.setWindowIcon(QIcon('IMAGES/BLU-LOGO.png'))
    window.setWindowTitle('BLU | VI')
    window.show()
    sys.exit(app.exec())
