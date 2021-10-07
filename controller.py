from abc import abstractmethod
import sys
from PyQt5.QtWidgets import (QApplication, QDialog, QDialogButtonBox, QMainWindow, QPushButton, QStackedLayout, QMessageBox, QLabel, QVBoxLayout, QHBoxLayout, QWidget)
from PyQt5.QtCore import (QThread, pyqtSignal)
from gui_groupchat import GroupchatBox
from alertbox import show_error_message
from gui_invite import InviteDialog
from gui_unconnected import UnconnectedWidget, Worker
from gui_connected import LIST_CHAT_ROOMS, LIST_CONNECTED_CLIENTS, ConnectedWidget
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
        self.connected: ConnectedWidget= ConnectedWidget(self)
        self.chatbox =  ChatBox(self)
        self.groupchatbox = GroupchatBox(self)
        self.pages = [self.unconnected,self.connected,self.chatbox, self.groupchatbox]

        self.stack = QStackedLayout()
        self.stack.addWidget(self.pages[PAGE_UNCONNECTED])
        self.stack.addWidget(self.pages[PAGE_CONNECTED])
        self.stack.addWidget(self.pages[PAGE_CHAT])
        self.stack.addWidget(self.pages[PAGE_GROUPCHAT])

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

        def someone_created_group(msg: str):
            # change model
            self.model.handle_group_creation(msg)
            self.connected.update_listview(
                LIST_CHAT_ROOMS,
                self.model.get_groups()
            )

        def someone_joined_the_group(msg: str):
            print("this is reached!")
            # TODO: change model
            self.model.handle_someone_joined_group(msg)
            # TODO: update participant list in group chat window
            self.groupchatbox.update_participant_list(msg.split(sep)[SENUM_SOMEONEJOINEDGROUP_GROUPNAME])
        
        def someone_sent_a_groupmessage(msg: str):
            self.model.handle_broadcasted_group_message(msg)
            self.groupchatbox.update_messagelist()

        def someone_joined_the_app(msg):
            user_list = msg.split(sep)[SENUM_USERLIST_USERS].split(";")

            for user in user_list:
                if user not in self.model.indiv_chat_dict:
                    self.model.indiv_chat_dict[user] = []

            self.connected.update_listview(
                LIST_CONNECTED_CLIENTS,
                user_list
            )

        def someone_invited_me_to_a_group(msg):
            # show a dialog, asking whether I want to join
            invitation_dialog = InvitationAcceptDeclineDialog(self.connected,self,msg)
            invitation_dialog.show()

        worker.signal_initialize.connect(lambda msg: moving_to_connect(msg))
        worker.signal_member_added.connect(lambda msg: someone_joined_the_app(msg))
        worker.signal_chat_individual.connect(lambda msg: someone_sent_me_message(msg))
        worker.signal_group_added.connect(lambda msg: someone_created_group(msg))
        worker.signal_group_member_added.connect(lambda msg: someone_joined_the_group(msg))
        worker.signal_chat_group.connect(lambda msg: someone_sent_a_groupmessage(msg))
        worker.signal_groupchat_invitation.connect(lambda msg: someone_invited_me_to_a_group(msg))
        

    def changePageTo(self,index):
        self.stack.setCurrentIndex(index)


    def chatwith(self, indivtochat):
        # TODO feedback: if indivtochat is empty, tell user to select a user to chat.
        if indivtochat is not None:
            self.chatbox.setChatWith(indivtochat)
            self.chatbox.setGeometry(self.connected.geometry())
            self.changePageTo(PAGE_CHAT)
        else:
            show_error_message("Make sure to select a person to 1:1 chat with")


    def exitTheApp(self):
        # do cleanup, notifying the server that it finished (so other clients can be notified)
        sys.exit()

    def getmodel(self) -> Model:
        return self.model


class InvitationAcceptDeclineDialog(QDialog):
    def __init__(self, parent, controller: ControllerBase, msg):
        super().__init__(parent)
        # this message corresponds to the invitation message sent by another client
        self.msg: str = msg
        self.controller: Controller = controller
        self.model : Model= controller.model
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("You are invited"))

        hbox = QHBoxLayout()
        btn_accept = QPushButton("Accept")
        btn_decline = QPushButton("Decline")

        def handle_accept():
            # handle a message from another client
            msg_parts = self.msg.split(sep)
            groupname = msg_parts[CENUM_GROUPINVITATION_GROUPNAME]
            self.hide()
            self.controller.changePageTo(PAGE_GROUPCHAT)
            self.controller.groupchatbox.current_group_number = groupname
            self.model.join_group(None, groupname)
    
        btn_accept.clicked.connect(lambda: handle_accept())
        btn_decline.clicked.connect(lambda: self.hide())
        hbox.addWidget(btn_accept)
        hbox.addWidget(btn_decline)

        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        self.setWindowTitle('Connection Page')
        self.setGeometry(300, 300, 200, 200)



if __name__ == '__main__':
    app = QApplication(sys.argv)

    controller = Controller()
    mainwindow = QMainWindow()
    mainwindow.setLayout(controller.stack)

    sys.exit(app.exec_())

