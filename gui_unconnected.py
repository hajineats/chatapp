import sys
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QVBoxLayout, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QPushButton)
from constants import *
from base import ControllerBase


WINDOW_WIDTH = 500
WINDOW_HEIGHT = 400
class MyApp(QWidget):

    def __init__(self, controller: ControllerBase,id="1"):
        super().__init__()
        self.controller = controller
        self.initUI(id)

    def initUI(self, id):
        # make footer
        connect_btn = QPushButton("Connect", self)
        connect_btn.clicked.connect(lambda: self.controller.changePageTo(PAGE_CONNECTED))
        cancel_btn = QPushButton("Cancel", self)
        cancel_btn.clicked.connect(lambda: self.controller.exitTheApp())
        hbox = QHBoxLayout()
        hbox.addStretch(10)
        hbox.addWidget(connect_btn)
        hbox.addWidget(cancel_btn)
        hbox.addStretch(1)

        # make textfields (IP address, port, nickname)
        tf_grid = QGridLayout()
        ip_tf = QLineEdit()
        port_tf = QLineEdit()
        nickname_tf = QLineEdit()
        tf_grid.addWidget(QLabel('IP address: '), 0, 0)
        tf_grid.addWidget(QLabel('Port: '), 1, 0)
        tf_grid.addWidget(QLabel('Nickname: '), 2, 0)
        tf_grid.addWidget(ip_tf, 0, 1)
        tf_grid.addWidget(port_tf, 1, 1)
        tf_grid.addWidget(nickname_tf, 2, 1)

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