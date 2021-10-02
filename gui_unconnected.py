import sys
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QVBoxLayout, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QPushButton)
from PyQt5.QtCore import (QThread, pyqtSignal)
from constants import *
from base import ControllerBase
from socket import socket
import socket as socket_module
import time

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
    signal_member_added = pyqtSignal(str)

    def __init__(self, socket_to_use:socket, unconnectedWidget,parent=None):
        super(Worker, self).__init__(parent)
        self.working = True
        self.socket = socket_to_use
        self.unconnectedWidget : UnconnectedWidget = unconnectedWidget


    def __det__(self):
        self.working = False
        self.wait()

    def run(self):
        self.unconnectedWidget.l_status.setText("this kinda runs?")
        bool = False
        # receive
        while True:
            try:
                if not bool:
                    message = self.socket.recv(BUFSIZE).decode()
                    # check message, then emit signal
                    if message:
                        print(message)
                        self.signal_initialize.emit(str(message))
                        bool = True
                

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
                # self.controller.changePageTo(PAGE_CONNECTED)

                # set up socket
                self.socket = socket(socket_module.AF_INET, socket_module.SOCK_STREAM)
                self.socket.connect((ip_addr, port))
                print(self.socket.recv(1024).decode())
                
                self.nickname = nickname
                # set up worker
                self.worker = Worker(self.socket, self)
                self.worker.signal_initialize.connect(lambda: self.l_status.setText("something did indeed happen!"))
                self.worker.start()


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