from abc import abstractmethod
import sys
from PyQt5.QtWidgets import (QApplication, QStackedLayout)
from PyQt5.QtCore import (QThread, pyqtSignal)
from gui_unconnected import UnconnectedWidget, Worker
from gui_connected import ConnectedWidget
from gui_frag_chatbox import ChatBox
from constants import *
from controller_interface import ControllerBase
import socket

BUFSIZE = 1024

class Controller(ControllerBase):
    def __init__(self):
        # initialize pages
        unconnected = UnconnectedWidget(self)
        connected = ConnectedWidget(self)
        chatbox =  ChatBox(self)
        pages = [unconnected,connected,chatbox]

        self.stack = QStackedLayout()
        self.stack.addWidget(pages[PAGE_UNCONNECTED])
        self.stack.addWidget(pages[PAGE_CONNECTED])
        self.stack.addWidget(pages[PAGE_CHAT])
        self.stack.setCurrentIndex(PAGE_UNCONNECTED)
        pass

    def setup_signal_handler(self, worker: Worker):
        worker.signal_initialize.connect(lambda msg: self.changePageTo(PAGE_CONNECTED))

    def changePageTo(self,index):
        self.stack.setCurrentIndex(index)

    def exitTheApp(self):
        # do cleanup, notifying the server that it finished (so other clients can be notified)
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    Controller()
    sys.exit(app.exec_())

