from abc import abstractmethod
import sys
from PyQt5.QtWidgets import (QApplication, QStackedLayout)
from PyQt5.QtCore import (QThread, pyqtSignal)
from gui_unconnected import UnconnectedWidget, Worker
from gui_connected import LIST_CONNECTED_CLIENTS, ConnectedWidget
from gui_frag_chatbox import ChatBox
from constants import *
from controller_interface import ControllerBase
from comm_enum import *
from model import Model
import socket

class Controller(ControllerBase):
    def __init__(self):
        # initialize pages
        self.model = Model()
        self.unconnected = UnconnectedWidget(self)
        self.connected = ConnectedWidget(self)
        self.chatbox =  ChatBox(self)
        pages = [self.unconnected,self.connected,self.chatbox]
        
        self.stack = QStackedLayout()
        self.stack.addWidget(pages[PAGE_UNCONNECTED])
        self.stack.addWidget(pages[PAGE_CONNECTED])
        self.stack.addWidget(pages[PAGE_CHAT])
        self.stack.setCurrentIndex(PAGE_UNCONNECTED)
        pass

    def setup_signal_handler(self, worker: Worker):
        worker.signal_initialize.connect(lambda msg: self.changePageTo(PAGE_CONNECTED))
        worker.signal_member_added.connect(lambda msg: self.connected.update_listview(
            LIST_CONNECTED_CLIENTS,
            msg.split(sep)[SENUM_USERLIST_USERS].split(";")))

    def changePageTo(self,index):
        self.stack.setCurrentIndex(index)


    def chatwith(self, indivtochat):
        # TODO feedback: if indivtochat is empty, tell user to select a user to chat.
        if indivtochat is not None:
            self.chatbox.setChatWith(indivtochat)
            self.changePageTo(PAGE_CHAT)

    def exitTheApp(self):
        # do cleanup, notifying the server that it finished (so other clients can be notified)
        sys.exit()

    def getmodel(self) -> Model:
        return self.model


if __name__ == '__main__':
    app = QApplication(sys.argv)

    Controller()
    sys.exit(app.exec_())

