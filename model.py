from socket import socket
from comm_enum import *

class Model():
    def __init__(self) -> None:
        self.socket :socket = None


        # for 1:1 chat. key is sockname (recipient), list is the list of messages
        self.indiv_chat_dict: dict[str, list[str]] = {}
        # for group chat. key is group identifier
        self.group_chat_dict: dict[str, list[str]] = {}

    def add_indiv_message(self, sockname:str, message):
        # send this message to server
        # sockname_excludenickname = sockname.split("@")[1]
        sender_nicksockname = f"{self.nickname}@{self.socket.getsockname()}"
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
        