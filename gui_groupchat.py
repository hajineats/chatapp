import sys
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QListView, QListWidget, QTextBrowser, QVBoxLayout, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QPushButton)
from PyQt5.QtCore import Qt
from constants import *
from controller_interface import ControllerBase
from gui_invite import InviteDialog
from server import Group
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 400

LIST_CONNECTED_CLIENTS = 0
LIST_CHAT_ROOMS = 1

class GroupchatBox(QWidget):
    def __init__(self, controller: ControllerBase):
        super().__init__()
        # who you are chatting with
        self.chatting_entity = None
        # the chat window
        self.chat_browser = None
        self.message_edit = None
        # TODO: change current group number when you go into the page of one group chat
        self.current_group_number = None

        # controller, model
        self.controller = controller
        self.model = controller.getmodel()
        
        self.initUI()

    # refresh the chat
    def update_messagelist(self):
        self.chat_browser.clear()

        msg_list: list[str] = self.model.group_chat_dict[self.model.get_group_by_id_groupnumber(self.current_group_number)]
        for msg in msg_list:
            self.chat_browser.append(msg)

    def createChatWindow(self):
        # HBOX (user input)
        if True:
            hbox = QHBoxLayout()
            self.message_edit = QLineEdit()

            def send_message():
                # send message
                self.model.broadcast_a_group_message(self.current_group_number,self.message_edit.text())
                self.update_messagelist()
                # self.model.add_indiv_message(self.chatting_entity, self.message_edit.text())
                # self.setChatWith(self.chatting_entity)

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
            def go_back_to_waitingroom():
                self.controller.connected.setGeometry(self.controller.chatbox.geometry())
                self.controller.changePageTo(PAGE_CONNECTED)

            close_btn.clicked.connect(lambda: go_back_to_waitingroom())
            vbox.addWidget(close_btn)
            return vbox

    def update_participant_list(self, group_number):
        # TODO see if the group number is the current group number
        if group_number is self.current_group_number:
            self.browser_member_list.clear()
            group:Group = self.model.get_group_by_id_groupnumber(group_number)
            for participant in group.participants:
                isMe = self.model.get_my_nicksockname().startswith(participant.strip())
                isHost = group.creator_nicksockname.startswith(participant.strip())

                participant = participant.split("@")[0]

                if isMe and isHost:
                    participant = f"[Me/Host] {participant}"
                elif isMe:
                    participant = f"[Me] {participant}"
                elif isHost:
                    participant = f"[Host] {participant}"

                self.browser_member_list.append(participant)

    def initUI(self):
        self.browser_member_list = QTextBrowser()
        # browser_member_list.append("Alice (host)")
        # browser_member_list.append("Bob")
        # browser_member_list.append("Craig (Me)")
        
        vbox_member_list = QVBoxLayout()
        vbox_member_list.addWidget(QLabel("Members"))
        vbox_member_list.addWidget(self.browser_member_list)
        btn_invite = QPushButton("Invite")
        vbox_member_list.addWidget(btn_invite)

        def popup_invite_dialog():
            invite_dialog = InviteDialog(self, self.controller, self.current_group_number)
            invite_dialog.show()
            pass

        btn_invite.clicked.connect(popup_invite_dialog)


        hbox = QHBoxLayout()
        hbox.addLayout(self.createChatWindow())
        hbox.addLayout(vbox_member_list)
        hbox.setStretch(0, 10)
        hbox.setStretch(1, 4)

        self.setLayout(hbox)
        self.setWindowTitle('Connection Page')
        self.setGeometry(300, 300, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.show()


