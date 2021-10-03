import sys
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QListView, QListWidget, QTextBrowser, QVBoxLayout, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QPushButton)
from PyQt5.QtCore import Qt
from constants import *

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 400

LIST_CONNECTED_CLIENTS = 0
LIST_CHAT_ROOMS = 1

class ChatBox(QWidget):

    def __init__(self):
        super().__init__()
        self.chatting_entity = None
        self.chat_browser = None
        self.message_edit = None
        # self.initUI()


    # refresh the chat
    def setChatWith(self, others_sockname):
        self.chatting_entity = others_sockname
        self.chat_browser.clear()

        msg_list: list[str] = self.model.get_indiv_message(self.chatting_entity)
        for msg in msg_list:
            self.chat_browser.append(msg)

    def createChatWindow(self):
        # HBOX (user input)
        if True:
            hbox = QHBoxLayout()
            self.message_edit = QLineEdit()

            def send_message():
                # send message
                self.model.add_indiv_message(self.chatting_entity, self.message_edit.text())
                self.setChatWith(self.chatting_entity)

            send_btn = QPushButton("Send", self)
            send_btn.clicked.connect(send_message)
            
            hbox.addWidget(self.message_edit)
            hbox.addWidget(send_btn)

        # VBOX (chat window)
        if True:
            vbox = QVBoxLayout()
            vbox.addWidget(QLabel("Chat with Alice"))
            self.chat_browser = QTextBrowser()
            
            vbox.addWidget(self.chat_browser)
            vbox.addLayout(hbox)
            close_btn = QPushButton("Close")
            vbox.addWidget(close_btn)
            return vbox



    # def initUI(self):
    #     self.setLayout(self.createChatWindow())
    #     self.setWindowTitle('Connection Page')
    #     self.setGeometry(300, 300, WINDOW_WIDTH, WINDOW_HEIGHT)
    #     self.show()

class GroupchatWrapper(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        browser_member_list = QTextBrowser()
        browser_member_list.append("Alice (host)")
        browser_member_list.append("Bob")
        browser_member_list.append("Craig (Me)")
        
        vbox_member_list = QVBoxLayout()
        vbox_member_list.addWidget(QLabel("Members"))
        vbox_member_list.addWidget(browser_member_list)
        vbox_member_list.addWidget(QPushButton("Invite"))

        hbox = QHBoxLayout()
        hbox.addLayout(ChatBox().createChatWindow())
        hbox.addLayout(vbox_member_list)
        hbox.setStretch(0, 10)
        hbox.setStretch(1, 4)

        self.setLayout(hbox)
        self.setWindowTitle('Connection Page')
        self.setGeometry(300, 300, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    page = GroupchatWrapper()
    sys.exit(app.exec_())
