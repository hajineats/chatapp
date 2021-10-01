from abc import abstractmethod
import sys
from PyQt5.QtWidgets import (QApplication, QStackedLayout)
from gui_unconnected import MyApp
from gui_connected import ConnectedWidget
from gui_frag_chatbox import ChatBox
from constants import *
from base import ControllerBase


class Controller(ControllerBase):
    def __init__(self):
        pages = [MyApp(self),ConnectedWidget(self), ChatBox(self)]
        self.stack = QStackedLayout()
        self.stack.addWidget(pages[PAGE_UNCONNECTED])
        self.stack.addWidget(pages[PAGE_CONNECTED])
        self.stack.addWidget(pages[PAGE_CHAT])
        self.stack.setCurrentIndex(PAGE_UNCONNECTED)
        pass

    def changePageTo(self,index):
        self.stack.setCurrentIndex(index)

    def exitTheApp(self):
        # do cleanup, notifying the server that it finished (so other clients can be notified)
        sys.exit()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    Controller()
    sys.exit(app.exec_())