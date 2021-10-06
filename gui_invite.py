import sys
from PyQt5.QtWidgets import (QDialog, QApplication, QHBoxLayout, QListView, QListWidget, QVBoxLayout, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QPushButton)
from PyQt5.QtCore import Qt
from model import Model
from server import Group
from controller_interface import ControllerBase

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 400

class InviteDialog(QDialog):
    def __init__(self, parent, controller: ControllerBase, cb, current_group_number):
        super().__init__(parent)
        self.controller = controller
        self.model: Model = controller.model
        self.current_group_number = current_group_number
        self.initUI()
        self.invitable_listview = None

        # self.model = model

    def update_list(self):
        connected_ppl: list[str] = self.model.indiv_chat_dict.keys()
        current_group: Group = self.model.get_group_by_id_groupnumber(self.current_group_number)
        
        invitable_ppl = []

        for person in connected_ppl:
            if not current_group.participants.__contains__(person):
                invitable_ppl.append(person)
        
        self.invitable_listview.addItems(invitable_ppl)
        self.invitable_listview.itemClicked.connect(lambda x: print(x.text()))


        pass
        # self.model.getListOfThoseNotInGroupchat()

    def initUI(self):
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("Connected Clients"))
        self.invitable_listview = QListWidget()

        self.update_list()
        vbox.addWidget(self.invitable_listview)

        hbox = QHBoxLayout()
        btn_invite = QPushButton("Invite")
        
        btn_cancel = QPushButton("Cancel")
        hbox.addWidget(btn_invite)
        hbox.addWidget(btn_cancel)

        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        self.setWindowTitle('Connection Page')
        self.setGeometry(300, 300, 200, WINDOW_HEIGHT)


# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         hbox = QHBoxLayout()
#         popDialog = QPushButton("hello")
#         hbox.addWidget(popDialog)

#         def showDialog():
#             invite=InviteDialog(self)
#             invite.show()

#         popDialog.clicked.connect(showDialog)

#         self.setLayout(hbox)
#         self.setWindowTitle('Connection Page')
#         self.setGeometry(300, 300, WINDOW_WIDTH, WINDOW_HEIGHT)
#         self.show()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     a = MainWindow()
#     sys.exit(app.exec_())