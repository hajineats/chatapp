import socket
from threading import Thread
from typing import final
from comm_enum import *
import time
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 10000 
separator_token = "<SEP>" # we will use this to separate the client name & message

class User():
    def __init__(self, nickname, sockname) -> None:
        self.nickname = nickname
        self.sockname = sockname
    
    def __hash__(self) -> int:
        return hash((self.nickname, self.sockname))
        
    def __eq__(self, o: object) -> bool:
        if isinstance(o, User):
            return self.nickname==o.nickname and self.sockname==o.sockname
        return False

    def __str__(self) -> str:
        return f"{self.nickname}@{self.sockname}"

class Group():
    def __init__(self, nicksockname="", room_number="") -> None:
        self.creator_nicksockname = nicksockname
        self.room_number = room_number
        # nicksockname of participants
        self.participants: list[str] = []
        pass

    def __hash__(self) -> int:
        return hash(self.room_number)
    
    def __eq__(self, o: object) -> bool:
        if isinstance(o, Group):
            return self.room_number==o.room_number
        return False

    def __str__(self) -> str:
        participants_concat = "|".join(self.participants)
        return f"{self.creator_nicksockname}@{self.room_number}@{participants_concat}"

class Server():
    def __init__(self) -> None:
        self.users = set()
        # str here refers to User#port
        self.client_sockets: dict[str, socket.socket] = {}
        self.configurate_socket()
        # key: group number, value: group object
        self.groups: dict[int,Group] = {}
        self.group_number = 0
    
    def add_user(self, new_user: User):
        self.users.add(new_user)


    def configurate_socket(self):
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((SERVER_HOST, SERVER_PORT))
        self.s.listen(5)
        print(f"[*] Listening as {self.s.getsockname()}")

    def listen_for_client(self, cs: socket.socket):
        while True:
            try:
                msg = cs.recv(1024).decode()
                print("[SERVER]:",msg)
            except Exception as e:
                # client no longer connected
                print(f"[!] Error: {e}")
                self.client_sockets.remove(cs.getsockname)

            # Message for client configuration
            if msg.startswith(CENUM_START_OF_MESSAGE+sep+CENUM_CLIENT_CONFIG):
                msg_parts = msg.split(sep)
                # client config message format
                if not len(msg_parts) == 4:
                    cs.send("Client configuration error: Message format is not supported")
                    continue
                
                # create user
                new_user = User(msg_parts[CENUM_CLIENT_CONFIG_NICKNAME], msg_parts[CENUM_CLIENT_CONFIG_SOCKNAME])
                self.add_user(new_user)
                print(msg)
                # echo message back on user creation success
                cs.send(msg.encode())
                # send user list to everyone
                self.sendtoeveryone_user_list()
                continue

            # client sent a message to another client
            if msg.startswith(CENUM_START_OF_MESSAGE+sep+CENUM_INDIVIDUALMESSAGE):
                msg_parts = msg.split(sep)
                if len(msg_parts) is not CENUM_INDIVIDUALMESSAGE_len:
                    cs.send("Individual message error: Message format is not supported".encode())
                    continue
                
                message_to_send = msg_parts[CENUM_INDIVIDUALMESSAGE_MESSAGE]
                socket_to_send_message_to = msg_parts[CENUM_INDIVIDUALMESSAGE_RECEIVER_SOCKET].split("@")[1]

                # send message to the receiver socket
                self.client_sockets[socket_to_send_message_to].send(
                    f"{CENUM_START_OF_MESSAGE}{sep}{CENUM_RCV_INDIVIDUALMESSAGE}{sep}{msg_parts[CENUM_INDIVIDUALMESSAGE_SENDER_SOCKET]}{sep}{message_to_send}".encode()
                )
                continue

            msg_parts = msg.split(sep)
            # client sends a message to create a group
            if msg_parts[MSG_TYPE] == CENUM_CREATEGROUP:
                # create a group object and change server state
                new_group = Group(msg_parts[CENUM_CREATEGROUP_CREATORNICKSOCK], self.group_number)
                self.groups[self.group_number] = new_group
                # print("DEBUG", self.group_number)
                # print("DBUG", new_group)
                # create a senum message to broadcast to everyone
                grouplist = ";".join(map(lambda x: str(x), self.groups.values()))
                grouplist = f"{CENUM_START_OF_MESSAGE}{sep}{SENUM_GROUPCREATED}{sep}{msg_parts[CENUM_CREATEGROUP_CREATORNICKSOCK]}{sep}{self.group_number}"
                for key in self.client_sockets:
                    self.client_sockets[key].send(grouplist.encode())


                # increment group number
                self.group_number = self.group_number + 1

            # client says I want to join a group
            if msg_parts[MSG_TYPE] == CENUM_JOINGROUP:
                for g in self.groups:
                    print("[DEBUG]", g)
                # find the group with group number
                group: Group = self.groups[int(msg_parts[CENUM_JOINGROUP_GROUPNAME])]
                
                # add him as a participant
                group.participants.append(msg_parts[CENUM_JOINGROUP_JOINERNICKSOCK])

                # send the group object (that includes list of participants) to everyone
                msg_to_send = str(group)
                msg_to_send = f"{CENUM_START_OF_MESSAGE}{sep}{SENUM_SOMEONEJOINEDGROUP}{sep}{group.room_number}{sep}{msg_to_send}"

                for participant_nicksock in group.participants:
                    participant_socket = self.client_sockets[participant_nicksock.split("@")[1]]
                    participant_socket.send(msg_to_send.encode())


            # for key in self.client_sockets:
            #     msg = msg.replace(separator_token, ": ")
            #     self.client_sockets[key].send(msg.encode())

    def sendtoeveryone_user_list(self):
        print(map(lambda x: f"{x.nickname}@{x.sockname}", self.users))
        userlist = ";".join(map(lambda x: str(x), self.users))
        userlist = f"{CENUM_START_OF_MESSAGE}{sep}{SENUM_USERLIST}{sep}{userlist}"
        for key in self.client_sockets:
            self.client_sockets[key].send(userlist.encode())
    


    def block_for_connection(self):
        while True:
            client_socket, client_address = self.s.accept()
            print(f"[+] {client_address} connected.")

            # socket_stringified = str(client_socket.getsockname())
            self.client_sockets[str(client_address)] = client_socket
            t = Thread(target=self.listen_for_client, args=(client_socket,))
            t.daemon = True
            t.start()
    
    def finish_server(self):
        for key in self.client_sockets:
            self.client_sockets[key].close()
        self.s.close()        





if __name__ == '__main__':
    server:Server = None
    try:
        server = Server()
        server.block_for_connection()
    finally:
        server.finish_server()



