import socket
from threading import Thread
from typing import final
from comm_enum import *

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 10000 
separator_token = "<SEP>" # we will use this to separate the client name & message

class User():
    def __init__(self, nickname, port) -> None:
        self.nickname = nickname
        self.port = port
    
    def __hash__(self) -> int:
        return hash((self.nickname, self.port))
        
    def __eq__(self, o: object) -> bool:
        if isinstance(o, User):
            return self.nickname==o.nickname and self.port==o.port
        return False

class Server():
    def __init__(self) -> None:
        self.users = set()
        self.client_sockets: dict[str, socket.socket] = {}
        self.configurate_socket()
        pass
    
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
            except Exception as e:
                # client no longer connected
                print(f"[!] Error: {e}")
                self.client_sockets.remove(cs.getsockname)
            
            # socket to send message to
            

            # client just started
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
                cs.send(f"{msg_parts[CENUM_CLIENT_CONFIG_NICKNAME]}, you are online now!".encode())
                continue

            for key in self.client_sockets:
                msg = msg.replace(separator_token, ": ")
                self.client_sockets[key].send(msg.encode())


    def block_for_connection(self):
        while True:
            client_socket, client_address = self.s.accept()
            print(f"[+] {client_address} connected.")
            self.client_sockets[client_socket.getsockname] = client_socket
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



