from socket import socket
from comm_enum import *
from server import Group
class Model():
    def __init__(self) -> None:
        self.socket :socket = None


        # for 1:1 chat. key is sockname (recipient), list is the list of messages
        self.indiv_chat_dict: dict[str, list[str]] = {}
        # for group chat. key is group, list is the list of messages
        self.group_chat_dict: dict[Group, list[str]] = {}

    def get_my_nicksockname(self):
        return f"{self.nickname}@{self.socket.getsockname()}"

    def add_indiv_message(self, sockname:str, message):
        # send this message to server
        # sockname_excludenickname = sockname.split("@")[1]
        sender_nicksockname = self.get_my_nicksockname()
        msg_to_send = f"{CENUM_START_OF_MESSAGE}{sep}{CENUM_INDIVIDUALMESSAGE}{sep}{sender_nicksockname}{sep}{sockname}{sep}{message}"
        self.socket.send(msg_to_send.encode())
        
        # is this a new message?
        if sockname not in self.indiv_chat_dict:
            self.indiv_chat_dict[sockname] = []
        print("[DEBUG][MODEL]:",self.indiv_chat_dict[sockname])
        self.indiv_chat_dict[sockname].append(message)
        print("---")

    def add_remote_indiv_message(self, sockname: str, message):
        # is this a new message?
        if sockname not in self.indiv_chat_dict:
            self.indiv_chat_dict[sockname] = []
        
        self.indiv_chat_dict[sockname].append(f"The other guy: {message}")
        print("[MODEL]:", self.indiv_chat_dict[sockname])
        print("---")


    def get_indiv_message(self, sockname):
        if sockname not in self.indiv_chat_dict:
            return []
        print("---")
        return self.indiv_chat_dict[sockname]

    # message is sent from the client that created the group
    def create_group(self):
        msg_to_send = f"{CENUM_START_OF_MESSAGE}{sep}{CENUM_CREATEGROUP}{sep}{self.get_my_nicksockname()}"
        self.socket.send(msg_to_send.encode())


    # client (that didn't create the group) receives this message and updates it to its list
    def handle_group_creation(self, msg):
        msg_parts = msg.split(sep)
        groupname = msg_parts[SENUM_GROUPCREATED_GROUPNAME]
        creator_nicksock = msg_parts[SENUM_GROUPCREATED_CREATORNICKSOCK]
        
        new_group = Group(creator_nicksock,groupname)
        if new_group not in self.group_chat_dict:
            self.group_chat_dict[new_group] = []

    def get_groups(self):
        if not self.group_chat_dict:
            return []
        return map(lambda x: str(x), self.group_chat_dict.keys())

    def add_group_message(self):
        pass

    def add_remote_group_message(self):
        pass

    