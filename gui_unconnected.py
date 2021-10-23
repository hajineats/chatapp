import sys
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QVBoxLayout, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QPushButton)
from PyQt5.QtCore import (QThread, pyqtSignal)
from constants import *
from controller_interface import ControllerBase
from socket import socket
import socket as socket_module
from comm_enum import *
import ssl

def trap_exc_during_debug(*args):
    # when app raises uncaught exception, print info
    print(args)


# install exception hook: without this, uncaught exception would cause application to exit
sys.excepthook = trap_exc_during_debug


WINDOW_WIDTH = 500
WINDOW_HEIGHT = 400
BUFSIZE = 1024

class Worker(QThread):
    # signals
    signal_chat_individual = pyqtSignal(str)
    signal_chat_group = pyqtSignal(str)
    signal_initialize = pyqtSignal(str)
    # this is when a new person connects to the server (not to a group)
    signal_member_added = pyqtSignal(str)
    # this is when group is created
    signal_group_added = pyqtSignal(str)
    # this is when a person joins a group
    signal_group_member_added = pyqtSignal(str)
    # this is when you get a groupchat invitation
    signal_groupchat_invitation = pyqtSignal(str)

    def __init__(self, socket_to_use:socket, unconnectedWidget,parent=None):
        super(Worker, self).__init__(parent)
        self.working = True
        self.socket = socket_to_use
        self.unconnectedWidget = unconnectedWidget


    def __det__(self):
        self.working = False
        self.wait()

    def run(self):
        while True:
            try:
                message = self.socket.recv(BUFSIZE).decode()

                # separate messages (in case there are multiple messages)
                messages = message.split(CENUM_START_OF_MESSAGE)[1:]
                print("[WORKER]",message)
                
                for m in messages:
                    # start of message would have been gone in splition, so reappend that starting part
                    m = f"{CENUM_START_OF_MESSAGE}{m}"
                    print("[WORKER] Processing this message", m)
                    # check message, then emit signal
                    if m:
                        msg_parts = m.split(sep)
                        # Receive message about configuration success
                        if msg_parts[MSG_TYPE] == CENUM_CLIENT_CONFIG:
                            self.signal_initialize.emit(str(m))
                        
                        # TODO: receive message about updated list of users
                        if msg_parts[MSG_TYPE] == SENUM_USERLIST:
                            print("on it sir!", str(message))
                            self.signal_member_added.emit(str(m))

                        # Receive message about 1:1 message
                        if msg_parts[MSG_TYPE] == CENUM_RCV_INDIVIDUALMESSAGE:
                            # TODO: check length of msg_parts 
                            self.signal_chat_individual.emit(str(m))

                        # Receive message about new group
                        if msg_parts[MSG_TYPE] == SENUM_GROUPCREATED:
                            self.signal_group_added.emit(str(m))

                        # someone joined the group
                        if msg_parts[MSG_TYPE] == SENUM_SOMEONEJOINEDGROUP:
                            self.signal_group_member_added.emit(str(m))

                        # someone sent a group message
                        if msg_parts[MSG_TYPE] == CENUM_GROUPMESSAGE:
                            self.signal_chat_group.emit(str(m))

                        if msg_parts[MSG_TYPE] == CENUM_GROUPINVITATION:
                            self.signal_groupchat_invitation.emit(str(m))

                

            except Exception as e:
                print(e)
                break



class UnconnectedWidget(QWidget):
    def __init__(self, controller: ControllerBase):
        super().__init__()
        self.controller = controller
        self.initUI()

    def onConnect(self):
        ip_addr = self.ip_tf.text()
        port = self.port_tf.text()
        nickname = self.nickname_tf.text()
        if ip_addr and port and nickname:
            try:
                port = int(port)

                # set up socket
                server_sni_hostname = 'hi.com'
                server_cert = './key_cert/server.crt'
                client_cert = './key_cert/client.crt'
                client_key = './key_cert/client.key'
                context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
                context.load_cert_chain(certfile=client_cert, keyfile=client_key)
                context.set_ciphers('AES128-SHA')
                non_ssl_socket = socket_module.socket(socket_module.AF_INET, socket_module.SOCK_STREAM)
                self.socket = context.wrap_socket(non_ssl_socket, server_side=False, server_hostname=server_sni_hostname)
                self.socket.connect((ip_addr, port))
                print("SSL established. Peer: {}".format(self.socket.getpeercert()))

                
                self.nickname = nickname
                # set up worker
                self.worker = Worker(self.socket, self)
                self.controller.setup_signal_handler(self.worker)
                self.worker.start()

                self.controller.model.socket = self.socket
                self.controller.nickname = self.nickname
                self.controller.model.nickname = self.nickname

                # notify server about client config information
                config_msg = f"{CENUM_START_OF_MESSAGE}{sep}{CENUM_CLIENT_CONFIG}{sep}{self.nickname}{sep}{self.socket.getsockname()}"
                self.socket.send(config_msg.encode())

            except ValueError as e:
                self.l_status.setText("IP address should be in the correct format!")
                print(e)
            except ConnectionRefusedError as e:
                self.l_status.setText("Connection Refused! Enter valid server IP address")
                print(e)

    def initUI(self):
        # make footer
        connect_btn = QPushButton("Connect", self)
        connect_btn.clicked.connect(lambda: self.onConnect())
        
        cancel_btn = QPushButton("Cancel", self)
        cancel_btn.clicked.connect(lambda: self.controller.exitTheApp())
        hbox = QHBoxLayout()
        hbox.addStretch(10)
        hbox.addWidget(connect_btn)
        hbox.addWidget(cancel_btn)
        hbox.addStretch(1)

        # make textfields (IP address, port, nickname)
        tf_grid = QGridLayout()
        self.ip_tf = QLineEdit()
        self.ip_tf.setText("127.0.0.1")
        self.port_tf = QLineEdit()
        self.port_tf.setText("10000")
        self.nickname_tf = QLineEdit()
        self.nickname_tf.setText("Hajin")
        
        tf_grid.addWidget(QLabel('IP address: '), 0, 0)
        tf_grid.addWidget(QLabel('Port: '), 1, 0)
        tf_grid.addWidget(QLabel('Nickname: '), 2, 0)
        tf_grid.addWidget(self.ip_tf, 0, 1)
        tf_grid.addWidget(self.port_tf, 1, 1)
        tf_grid.addWidget(self.nickname_tf, 2, 1)

        # status display
        self.l_status = QLabel("")
        tf_grid.addWidget(self.l_status, 3, 0,1,2)


        # make container vbox
        container_vbox = QVBoxLayout()
        container_vbox.addStretch(1)
        container_vbox.addLayout(tf_grid)
        container_vbox.addStretch(1)
        container_vbox.addLayout(hbox)
        self.setLayout(container_vbox)
        
        self.setWindowTitle('Connection Page')
        self.setGeometry(300, 300, WINDOW_WIDTH, WINDOW_HEIGHT)
        # self.show()