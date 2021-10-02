from abc import abstractmethod
import sys
from PyQt5.QtWidgets import (QApplication, QStackedLayout)
from PyQt5.QtCore import (QThread, pyqtSignal)
from gui_unconnected import UnconnectedWidget
from gui_connected import ConnectedWidget
from gui_frag_chatbox import ChatBox
from constants import *
from base import ControllerBase
import socket

class Main():
    def __init__(self) -> None:
        self.connect()

    def connect(self):
        # create an unconnected page
        # on connect, create Worker 




if __name__ == '__main__':
    app = QApplication(sys.argv)

    Controller()
    sys.exit(app.exec_())