import sys
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QListView, QListWidget, QVBoxLayout, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QPushButton)
from PyQt5.QtCore import Qt
from constants import *
from controller_interface import ControllerBase
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 400

LIST_CONNECTED_CLIENTS = 0
LIST_CHAT_ROOMS = 1

class ConnectedWidget(QWidget):

    def __init__(self, controller: ControllerBase):
        super().__init__()
        self.controller = controller
        self.connected_clients_list = ["Alice", "Hajin"]
        self.chat_rooms_list = ["A", "B", "C"]
        self.make_two_lists()
        self.initUI()


    def initUI(self):
        # vbox{create, join}
        vbox = QVBoxLayout()
        vbox.addWidget(QPushButton("Create", self))
        vbox.addWidget(QPushButton("Join", self))
        
        
        grid = QGridLayout()
        # first row
        grid.addWidget(QLabel("Connected Clients"),0,0)
        grid.addWidget(self.listview[LIST_CONNECTED_CLIENTS],1,0)
        grid.addWidget(QPushButton("1 : 1 Chat", self),1,1,1,1, Qt.AlignTop)

        # second row
        grid.addWidget(QLabel("Chat rooms"), 2, 0)
        grid.addWidget(self.listview[LIST_CHAT_ROOMS], 3, 0)
        grid.addLayout(vbox, 3,1,1,1,Qt.AlignTop)

        # third row
        grid.addWidget(QPushButton("Cancel(Back)", self),4,1)

        # set stretch to layout
        grid.setColumnStretch(0,10)
        grid.setColumnStretch(1,4)

        self.setLayout(grid)
        self.setWindowTitle('Connection Page')
        self.setGeometry(300, 300, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.show()

    # Makes two list widgets:
    # one for displaying a list of connected clients
    # another for displaying a list of chat rooms
    def make_two_lists(self):
        # initialize two lists
        self.listview = []        
        self.listview.append(QListWidget())
        self.listview.append(QListWidget())

        # create list for connected clients 
        for i, v in enumerate(self.connected_clients_list):
            self.listview[LIST_CONNECTED_CLIENTS].insertItem(i, v)

        self.listview[LIST_CONNECTED_CLIENTS].clicked.connect(
            lambda: print(self.listview[LIST_CONNECTED_CLIENTS].currentItem().text())
        )

        # create list for chat rooms
        for i, v in enumerate(self.chat_rooms_list):
            self.listview[LIST_CHAT_ROOMS].insertItem(i, v)

        self.listview[LIST_CHAT_ROOMS].clicked.connect(
            lambda: print(self.listview[LIST_CHAT_ROOMS].currentItem().text())
        )


