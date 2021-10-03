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
        self.selected_indivtochat = None
        self.selected_grouptochat = None
        self.controller = controller
        self.model = self.controller.model
        self.connected_clients_list = ["lol huh", "huhhh"]
        self.chat_rooms_list = ["aw", "wa"]
        self.make_two_lists()
        self.initUI()


    def initUI(self):
        # vbox{create, join}
        vbox = QVBoxLayout()
        btn_create_group = QPushButton("Create", self)
        def create_group():
            self.model.create_group()

        btn_create_group.clicked.connect(create_group)
        vbox.addWidget(btn_create_group)
        vbox.addWidget(QPushButton("Join", self))
        
        
        self.grid = QGridLayout()
        # first row
        self.grid.addWidget(QLabel("Connected Clients"),0,0)
        self.grid.addWidget(self.listview[LIST_CONNECTED_CLIENTS],1,0)
        btn_start_indiv_chat = QPushButton("1 : 1 Chat", self)
        btn_start_indiv_chat.clicked.connect(lambda: self.controller.chatwith(self.selected_indivtochat))
        self.grid.addWidget(btn_start_indiv_chat,1,1,1,1, Qt.AlignTop)
        

        # second row
        self.grid.addWidget(QLabel("Chat rooms"), 2, 0)
        self.grid.addWidget(self.listview[LIST_CHAT_ROOMS], 3, 0)
        self.grid.addLayout(vbox, 3,1,1,1,Qt.AlignTop)

        # third row
        self.grid.addWidget(QPushButton("Cancel(Back)", self),4,1)

        # set stretch to layout
        self.grid.setColumnStretch(0,10)
        self.grid.setColumnStretch(1,4)

        self.setLayout(self.grid)
        self.setWindowTitle('Connection Page')
        self.setGeometry(300, 300, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.show()

    # Makes two list widgets:
    # one for displaying a list of connected clients
    # another for displaying a list of chat rooms
    def make_two_lists(self):
        # initialize two lists
        self.listview = [None, None]        
        self.listview[LIST_CONNECTED_CLIENTS] = self.generate_list_widget(self.connected_clients_list)
        self.listview[LIST_CHAT_ROOMS] = self.generate_list_widget(self.chat_rooms_list)

    def update_listview(self, list_index, new_list):
        print("i'm here!")
        print(new_list)
        self.listview[list_index] = self.generate_list_widget(new_list)
        self.listview[list_index].scrollToBottom()
        self.grid.addWidget(self.listview[list_index],2*list_index+1,0)


    def generate_list_widget(self, with_items):
        # TODO: add callback function as argument to customise what happens when an item is selected
        list_widget = QListWidget()

        for i, v in enumerate(with_items):
            list_widget.insertItem(i, v)
        
        def select_item():
            selected_text =list_widget.currentItem().text()
            self.selected_indivtochat = selected_text
            print("[LISTVIEW]",selected_text)

        list_widget.clicked.connect(lambda: select_item())
        return list_widget
    
    

