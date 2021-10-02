import sys
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QListView, QListWidget, QTextBrowser, QVBoxLayout, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QPushButton)
from PyQt5.QtCore import Qt
from constants import *
from controller_interface import ControllerBase
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 400

LIST_CONNECTED_CLIENTS = 0
LIST_CHAT_ROOMS = 1

class ChatBox(QWidget):

    def __init__(self, controller: ControllerBase):
        super().__init__()
        self.chatting_entity = None
        self.chat_browser = None
        self.controller = controller
        self.initUI()


    def setChatWith(self, chatting_entity):
        self.chatting_entity = chatting_entity
        

    def createChatWindow(self):

        # user input portion
        hbox = QHBoxLayout()
        message_edit = QLineEdit()
        send_btn = QPushButton("Send", self)
        hbox.addWidget(message_edit)
        hbox.addWidget(send_btn)

        # dynamic portion
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("Chat with Alice"))
        self.chat_browser = QTextBrowser()
        if self.chatting_entity is not None:
            # TODO populate self.chat_browser with data
            pass
            
        vbox.addWidget(self.chat_browser)
        vbox.addLayout(hbox)
        vbox.addWidget(QPushButton("Close"))
        return vbox

    def initUI(self):
        # hbox to write message and send
        self.setLayout(self.createChatWindow())
        self.setWindowTitle('Connection Page')
        self.setGeometry(300, 300, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.show()

    


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     page = ChatBox()
#     sys.exit(app.exec_())

