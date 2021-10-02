from abc import abstractmethod
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QStackedLayout)
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
        self.pages = [self.unconnected,self.connected,self.chatbox]



        self.stack = QStackedLayout()
        self.stack.addWidget(self.pages[PAGE_UNCONNECTED])
        self.stack.addWidget(self.pages[PAGE_CONNECTED])
        self.stack.addWidget(self.pages[PAGE_CHAT])
        self.stack.setCurrentIndex(PAGE_UNCONNECTED)
        pass

    def setup_signal_handler(self, worker: Worker):
        def moving_to_connect(msg: str):
            # unify location of connected window
            self.connected.setGeometry(self.unconnected.geometry())
            self.changePageTo(PAGE_CONNECTED)

        def someone_sent_me_message(msg: str):
            sender_sockname = msg.split(sep)[CENUM_RCV_INDIVIDUALMESSAGE_SENDER_SOCKET]
            sender_message = msg.split(sep)[CENUM_RCV_INDIVIDUALMESSAGE_MESSAGE]
            # add to cache
            self.model.add_remote_indiv_message(sender_sockname, sender_message)
            # update gui
            self.chatbox.setChatWith(sender_sockname)


        worker.signal_initialize.connect(lambda msg: moving_to_connect(msg))
        worker.signal_member_added.connect(lambda msg: self.connected.update_listview(
            LIST_CONNECTED_CLIENTS,
            msg.split(sep)[SENUM_USERLIST_USERS].split(";")))
        
        

        worker.signal_chat_individual.connect(lambda msg: someone_sent_me_message(msg))

    def changePageTo(self,index):
        self.stack.setCurrentIndex(index)


    def chatwith(self, indivtochat):
        # TODO feedback: if indivtochat is empty, tell user to select a user to chat.
        if indivtochat is not None:
            self.chatbox.setChatWith(indivtochat)
            self.chatbox.setGeometry(self.connected.geometry())
            self.changePageTo(PAGE_CHAT)

    def exitTheApp(self):
        # do cleanup, notifying the server that it finished (so other clients can be notified)
        sys.exit()

    def getmodel(self) -> Model:
        return self.model


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = Controller()
    mainwindow = QMainWindow()
    mainwindow.setLayout(controller.stack)
    
    sys.exit(app.exec_())

